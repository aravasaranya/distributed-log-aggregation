#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#define PORT 9000

int main()
{
    int server_socket;
    char message[1024];

    int total = 0;
    int info = 0;
    int warning = 0;
    int error = 0;
    int critical = 0;

    struct sockaddr_in server_address;
    struct sockaddr_in client_address;

    socklen_t client_length = sizeof(client_address);

    server_socket = socket(AF_INET, SOCK_DGRAM, 0);

    if (server_socket < 0)
    {
        printf("Socket creation failed\n");
        return 1;
    }

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(PORT);

    if (bind(server_socket, (struct sockaddr *)&server_address,
             sizeof(server_address)) < 0)
    {
        printf("Bind failed\n");
        close(server_socket);
        return 1;
    }

    printf("Log server started on port %d\n", PORT);

    while (1)
    {
        int n = recvfrom(server_socket, message, sizeof(message) - 1, 0,
                         (struct sockaddr *)&client_address,
                         &client_length);

        if (n < 0)
        {
            printf("Error receiving message\n");
            continue;
        }

        message[n] = '\0';

        char *host = strtok(message, "|");
        char *timestamp = strtok(NULL, "|");
        char *severity = strtok(NULL, "|");
        char *log_message = strtok(NULL, "");

        if (host && timestamp && severity && log_message)
        {
            total++;

            if (strcmp(severity, "INFO") == 0)
                info++;
            else if (strcmp(severity, "WARNING") == 0)
                warning++;
            else if (strcmp(severity, "ERROR") == 0)
                error++;
            else if (strcmp(severity, "CRITICAL") == 0)
                critical++;

            FILE *file = fopen("/home/saranya/sdn_log_project/logs.txt", "a");

            if (file != NULL)
            {
                fprintf(file, "%s|%s|%s|%s\n",
                        host, timestamp, severity, log_message);
                fclose(file);
            }

            printf("\n-----------------------------\n");
            printf("Host     : %s\n", host);
            printf("Timestamp: %s\n", timestamp);
            printf("Severity : %s\n", severity);
            printf("Message  : %s\n", log_message);
            printf("-----------------------------\n");

            printf("Total logs : %d\n", total);
            printf("INFO       : %d\n", info);
            printf("WARNING    : %d\n", warning);
            printf("ERROR      : %d\n", error);
            printf("CRITICAL   : %d\n", critical);
        }
        else
        {
            printf("Invalid log format\n");
        }
    }

    close(server_socket);

    return 0;
}
