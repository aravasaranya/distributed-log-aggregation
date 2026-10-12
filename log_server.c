#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 9000
#define BUFFER_SIZE 1024

int main()
{
    int sockfd;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    char buffer[BUFFER_SIZE];

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (sockfd < 0)
    {
        perror("socket");
        return 1;
    }

    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(sockfd, (struct sockaddr *)&server_addr,
             sizeof(server_addr)) < 0)
    {
        perror("bind");
        close(sockfd);
        return 1;
    }

    printf("UDP Log Server started on port %d\n", PORT);

    while (1)
    {
        int n = recvfrom(sockfd, buffer, BUFFER_SIZE - 1, 0,
                         (struct sockaddr *)&client_addr,
                         &client_len);

        if (n < 0)
        {
            perror("recvfrom");
            continue;
        }

        buffer[n] = '\0';

        char copy[BUFFER_SIZE];
        strcpy(copy, buffer);

        char *host = strtok(copy, "|");
        char *timestamp = strtok(NULL, "|");
        char *severity = strtok(NULL, "|");
        char *message = strtok(NULL, "");

        if (host && timestamp && severity && message)
        {
            printf("\n----- LOG RECEIVED -----\n");
            printf("Host      : %s\n", host);
            printf("Timestamp : %s\n", timestamp);
            printf("Severity  : %s\n", severity);
            printf("Message   : %s\n", message);
            printf("------------------------\n");
        }
        else
        {
            printf("\nInvalid log format: %s\n", buffer);
        }
    }

    close(sockfd);
    return 0;
}
