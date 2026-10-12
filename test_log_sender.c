#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Usage: %s <client_id>\n", argv[0]);
        return 1;
    }

    int client_id = atoi(argv[1]);

    int sockfd;
    struct sockaddr_in server_addr;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (sockfd < 0)
    {
        perror("socket");
        return 1;
    }

    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(9000);
    inet_pton(AF_INET, "127.0.0.1", &server_addr.sin_addr);

    const char *levels[] = {
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL"
    };

    for (int i = 0; i < 4; i++)
    {
        char log[512];

        snprintf(log, sizeof(log),
                 "client%d|2026-10-07 06:45:%02d|%s|Test application log message",
                 client_id, i, levels[i]);

        sendto(sockfd, log, strlen(log), 0,
               (struct sockaddr *)&server_addr,
               sizeof(server_addr));

        printf("Sent: %s\n", log);

        sleep(1);
    }

    close(sockfd);
    return 0;
}
