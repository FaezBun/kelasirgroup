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
    
    int bytes = recv(cfd, buffer, sizeof(buffer) - 1, 0);
    if (bytes > 0) {
        buffer[bytes] = '\0';
        MYSQL *conn = mysql_init(NULL);
        // Pastikan hostname "db" betul mengikut docker-compose service name
        if (mysql_real_connect(conn, "db", "root", "rootpassword", "socket_db", 3306, NULL, 0)) {
            char q[256];
            sprintf(q, "UPDATE user_points SET points = points + 1 WHERE user = '%s'", buffer);
            mysql_query(conn, q);
            mysql_close(conn);
        }
    }
    close(cfd);
    free(arg);
    return NULL;
}

int main() {
    int sfd = socket(AF_INET, SOCK_STREAM, 0);
    int port = atoi(getenv("PORT"));
    
    struct sockaddr_in addr = {AF_INET, htons(port), INADDR_ANY};
    bind(sfd, (struct sockaddr *)&addr, sizeof(addr));
    listen(sfd, 10);
    
    printf("Server listening on port %d...\n", port);

    while (1) {
        int *cfd = malloc(sizeof(int));
        *cfd = accept(sfd, NULL, NULL);
        pthread_t tid;
        pthread_create(&tid, NULL, handle_client, cfd);
        pthread_detach(tid);
    }
}
