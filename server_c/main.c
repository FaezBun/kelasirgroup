#include <mysql/mysql.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <arpa/inet.h>
#include <string.h>

void *handle_client(void *arg) {
    int cfd = *(int*)arg;
    char buffer[50];
    char point_str[50] = "0"; // Nilai lalai jika berlaku ralat
    
    int bytes = recv(cfd, buffer, sizeof(buffer) - 1, 0);
    if (bytes > 0) {
        buffer[bytes] = '\0';
        buffer[strcspn(buffer, "\r\n")] = 0; // Bersihkan newline jika ada
        
        printf("[SERVER C] Terima request dari ID: '%s'\n", buffer);

        MYSQL *conn = mysql_init(NULL);
        
        // Pastikan maklumat ini (db, root, rootpassword, socket_db) betul 
        // dengan konfigurasi docker-compose.yml anda!
        if (mysql_real_connect(conn, "db", "root", "rootpassword", "socket_db", 3306, NULL, 0)) {
            char q[256];
            
            // 1. UPDATE mata pengguna (+1)
            sprintf(q, "UPDATE user_points SET points = points + 1 WHERE user = '%s'", buffer);
            mysql_query(conn, q);
            
            // 2. SELECT mata terkini untuk dihantar ke client
            sprintf(q, "SELECT points FROM user_points WHERE user = '%s'", buffer);
            if (mysql_query(conn, q) == 0) {
                MYSQL_RES *res = mysql_store_result(conn);
                if (res) {
                    MYSQL_ROW row = mysql_fetch_row(res);
                    if (row && row[0]) {
                        strcpy(point_str, row[0]); // Simpan point ke dalam variable
                    }
                    mysql_free_result(res);
                }
            }
            mysql_close(conn);
        } else {
            printf("[SERVER C] Ralat: Gagal menyambung ke database!\n");
            strcpy(point_str, "Ralat DB");
        }
        
        // 3. Hantar point terkini BALIK kepada client
        send(cfd, point_str, strlen(point_str), 0);
        printf("[SERVER C] Point terkini (%s) dihantar kepada ID '%s'\n", point_str, buffer);
    }
    
    close(cfd);
    free(arg);
    return NULL;
}

int main() {
    // WAJIB: Matikan buffering supaya nampak log server di Docker
    setvbuf(stdout, NULL, _IONBF, 0);

    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    
    // Ambil PORT dari persekitaran, letak fallback (cth: 5000) jika kosong
    int port = getenv("PORT") ? atoi(getenv("PORT")) : 5000; 
    
    // Elak ralat "Address already in use" bila restart container
    int opt = 1;
    setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    struct sockaddr_in addr = {AF_INET, htons(port), INADDR_ANY};
    bind(sfd, (struct sockaddr *)&addr, sizeof(addr));
    listen(sfd, 10);
    
    printf("[SERVER C] Server listening on port %d...\n", port);

    while (1) {
        int *cfd = malloc(sizeof(int));
        *cfd = accept(sfd, NULL, NULL);
        
        // Cetak log bila ada client baru connect
        printf("[SERVER C] Client baru disambungkan!\n");
        
        pthread_t tid;
        pthread_create(&tid, NULL, handle_client, cfd);
        pthread_detach(tid);
    }
}
