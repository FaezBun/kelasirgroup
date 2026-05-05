#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netdb.h>
#include <string.h>
#include <arpa/inet.h>

int main() {
    char *host = getenv("TARGET_HOST");
    int port = atoi(getenv("TARGET_PORT"));
    char *uid = getenv("USER_ID"); // Ambil ID dari environment variable

    while(1) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        struct hostent *server = gethostbyname(host);
        
        if (server) {
            struct sockaddr_in srv = {AF_INET, htons(port)};
            memcpy(&srv.sin_addr.s_addr, server->h_addr, server->h_length);
            
            if (connect(sock, (struct sockaddr *)&srv, sizeof(srv)) == 0) {
                // HANTAR ID ke Server sebaik sahaja bersambung
                if (uid) {
                    send(sock, uid, strlen(uid), 0);
                }
            }
        }
        close(sock);
        sleep(10);
    }
}
