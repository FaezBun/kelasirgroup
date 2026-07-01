#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>

int main() {
    // 1. WAJIB: Matikan buffering supaya log terus dihantar ke Docker tanpa sangkut
    setvbuf(stdout, NULL, _IONBF, 0);

    char *host = getenv("TARGET_HOST");
    int port = atoi(getenv("TARGET_PORT"));
    char *uid = getenv("USER_ID"); // Ambil ID dari environment variable

    // Log permulaan untuk tahu client dah up
    printf("[CLIENT %s] Memulakan client... Sasaran: %s:%d\n", uid ? uid : "UNKNOWN", host, port);

    while(1) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        struct hostent *server = gethostbyname(host);
        
        if (server) {
            struct sockaddr_in srv = {AF_INET, htons(port)};
            memcpy(&srv.sin_addr.s_addr, server->h_addr, server->h_length);
            
            printf("[CLIENT %s] Cuba menyambung ke server...\n", uid ? uid : "UNKNOWN");
            
            if (connect(sock, (struct sockaddr *)&srv, sizeof(srv)) == 0) {
                printf("[CLIENT %s] Berjaya disambung! Menghantar ID...\n", uid ? uid : "UNKNOWN");
                
                // HANTAR ID ke Server sebaik sahaja bersambung
                if (uid) {
                    send(sock, uid, strlen(uid), 0);
                    
                    // 2. TERIMA POINT DB DARI SERVER
                    char rx_buffer[1024] = {0};
                    int bytes_received = recv(sock, rx_buffer, sizeof(rx_buffer) - 1, 0);
                    
                    if (bytes_received > 0) {
                        // Berjaya terima data point dari server
                        printf("[CLIENT %s] ID '%s' dihantar. Point DB Terkini: %s\n", uid, uid, rx_buffer);
                    } else {
                        // Server terputus atau tidak membalas dengan data point
                        printf("[CLIENT %s] ID dihantar, tiada respon point dari server.\n", uid);
                    }
                }
            } else {
                printf("[CLIENT %s] Gagal menyambung ke server (Connection refused).\n", uid ? uid : "UNKNOWN");
            }
        } else {
            printf("[CLIENT %s] Ralat: Hos '%s' tidak dijumpai.\n", uid ? uid : "UNKNOWN", host);
        }
        
        close(sock);
        printf("[CLIENT %s] Soket ditutup. Tunggu 10 saat sebelum cuba lagi...\n", uid ? uid : "UNKNOWN");
        printf("--------------------------------------------------\n");
        
        sleep(10);
    }
}
