#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void generate_log(char *log, int client_id, int level)
{
    const char *levels[] = {"INFO", "WARNING", "ERROR", "CRITICAL"};
    time_t now = time(NULL);
    struct tm *t = localtime(&now);

    strftime(log, 256, "%Y-%m-%d %H:%M:%S", t);

    char temp[256];
    snprintf(temp, sizeof(temp),
             "[%s] CLIENT-%d [%s] Application event generated",
             log, client_id, levels[level]);

    snprintf(log, 256, "%s", temp);
}
