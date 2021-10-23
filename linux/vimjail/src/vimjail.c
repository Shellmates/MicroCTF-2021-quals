#include <unistd.h>

void main(void){
    execl("/usr/bin/view", "/usr/bin/view", "/challenge/readme.txt", NULL);
}
