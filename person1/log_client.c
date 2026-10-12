#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>

void generate_log(char *log, int client_id, int level);

int main(int argc, char *argv[])
{
    if (argc < 5)
    {
        printf("Usage: %s <server_ip> <port> <client_id> <rate>\n", argv[0]);
        return 1;
    }

    char *server_ip = argv[1];
    int port = atoi(argv[2]);
    int client_id = atoi(argv[3]);
    int rate = atoi(argv[4]);

    if (rate <= 0)
        rate = 1;

    int sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (sockfd < 0)
    {
        perror("socket");
        return 1;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(port);

    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0)
    {
        printf("Invalid server IP\n");
        close(sockfd);
        return 1;
    }

    srand(time(NULL) + client_id);

    printf("Client %d started. Rate: %d logs/sec\n", client_id, rate);

    while (1)
    {
        char log[256];
        int level = rand() % 4;

        generate_log(log, client_id, level);

        sendto(sockfd, log, strlen(log), 0,
               (struct sockaddr *)&server_addr,
               sizeof(server_addr));

        printf("%s\n", log);

        usleep(1000000 / rate);
    }

    close(sockfd);
    return 0;
}
