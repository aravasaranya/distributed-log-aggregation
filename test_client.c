#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9000

int main()
{
    int sockfd;

    char *messages[] = {
        "h1|2026-10-06 12:20:00|ERROR|Database connection failed",
        "h1|2026-10-06 12:25:00|INFO|User logged in",
        "h2|2026-10-06 12:26:00|WARNING|CPU usage high",
        "h3|2026-10-06 12:27:00|CRITICAL|Server is down"
    };

    struct sockaddr_in server_address;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (sockfd < 0)
    {
        printf("Socket creation failed\n");
        return 1;
    }

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(PORT);
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");

    for (int i = 0; i < 4; i++)
    {
        sendto(sockfd, messages[i], strlen(messages[i]), 0,
               (struct sockaddr *)&server_address,
               sizeof(server_address));

        printf("Log sent: %s\n", messages[i]);

        sleep(1);
    }

    close(sockfd);

    return 0;
}
