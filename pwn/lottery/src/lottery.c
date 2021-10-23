#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define NICK_SIZE 32
#define BUFF_SIZE 16
#define MAX_ROUNDS 10

struct Player {
    unsigned long age;
    char gender[BUFF_SIZE];
    char *nickname;
};

struct Round {
    struct Round *next;
    unsigned int number;
    unsigned long value;
    unsigned long guess;
};

unsigned int seed;
struct Player *player = NULL;
struct Round *head = NULL;

void win() {
    execl("/bin/cat", "/bin/cat", "flag.txt", NULL);
}

unsigned int get_random_seed() {
    unsigned int seed;
    int fd = open("/dev/urandom", O_RDONLY);
    read(fd, &seed, sizeof(seed));
    close(fd);
    return seed;
}

void welcome() {
    puts(
        "   .--------------------------------------------.\n"
        "   |   WELCOME TO YOUR FAVOURITE LOTTERY GAME   |\n"
        "   | SECURE CODING IS HARD, BUT WE DID OUR BEST |\n"
        "   |   TO ENSURE A FAIR GAME FOR EVERYONE :)    |\n"
        "   `--------------------------------------------'\n"
        "                  /\n"
        "                 /\n"
        "         ,---')\n"
        "        (  -_-(\n"
        "        ) .__/ )\n"
        "      _/ _/_( /        _.---._\n"
        "     (__/ _ _) ,-._   /  o    \\\n"
        "       //)__(\\/,-` |_| O  o o O|\n"
        "   _\\\\///==o=\\'      |O o  o O |\n"
        "    `-' \\    /        \\O o   o/\n"
        "         )___\\         `'-.-\\\\\n"
        "        / ,\\ \\       ____)_(____\n"
        "       / /  \\ \\     '--..---,,--'\n"
        "      /()    >()        \\\\_//\n"
        "  hfz |\\_\\   |\\_\\       /,-.\\\n"
        "                 https://ascii.co.uk/art/lottery\n"
    );
}

unsigned long menu() {
    char buff[BUFF_SIZE];
    puts(
        ".--------- Menu ---------.\n"
        "| 1. Register            |\n"
        "| 2. Play                |\n"
        "| 3. Stats               |\n"
        "| 4. Unregister          |\n"
        "| 5. Quit                |\n"
        "`------------------------'"
    );
    printf(">>> ");
    fgets(buff, BUFF_SIZE, stdin);
    return strtoul(buff, NULL, 10);
}

void register_player(unsigned long age, char *gender, char *nickname) {
    player = malloc(sizeof(struct Player));
    player->nickname = malloc(NICK_SIZE);
    player->age = age;
    strncpy(player->gender, gender, BUFF_SIZE);
    strncpy(player->nickname, nickname, NICK_SIZE);
}

void unregister_player() {
    free(player->nickname);
    free(player);
}

void show_stats() {
    struct Round *round = head;
    if (!round) {
        puts("Nothing to show!");
        return;
    }
    printf(
        "Current player: Mr%s. %s, %lu year(s) old\n",
        strcmp(player->gender, "male") ? "s" : "", player->nickname, player->age
    );
    puts(".-------------------------------------------------------------.");
    puts("| Round number |      Your guess      |      Actual value     |");
    puts(":-------------------------------------------------------------:");
    while (round) {
        printf("| %12u | %20lu | %21lu |\n", round->number, round->guess, round->value);
        round = round->next;
    }
    puts("`-------------------------------------------------------------'");
}

void setup() {
    seed = get_random_seed();
    srand(seed);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    bool registered = false;
    unsigned long choice, value, guess;
    unsigned int age, round_number = 0;
    char nickname[NICK_SIZE], buff[BUFF_SIZE], *idx;
    setup();
    welcome();
    while (round_number < MAX_ROUNDS && (choice = menu()) != 5) {
        switch (choice) {
            case 1:
                if (registered) {
                    puts("You're already registered.");
                    break;
                }

                printf("Enter your age: ");
                fgets(buff, BUFF_SIZE, stdin);
                age = strtoul(buff, NULL, 10);
                if (age < 18) {
                    puts("Sorry kiddo, you're too young for this game :(");
                    break;
                }

                printf("Enter your gender (male/female): ");
                fgets(buff, BUFF_SIZE, stdin);
                if ((idx = strchr(buff, '\n')) != NULL) *idx = '\0';
                if (strcmp(buff, "male") && strcmp(buff, "female")){
                    puts("Hmm? You can either be a male or a female, aRe U a RoBoT??");
                    break;
                }

                printf("Enter your nickname: ");
                fgets(nickname, NICK_SIZE, stdin);
                if ((idx = strchr(nickname, '\n')) != NULL) *idx = '\0';

                register_player(age, buff, nickname);
                puts("Successfully registered.");
                registered = true;
                break;
            case 2:
                if (!player) {
                    puts("Please register first :)");
                    break;
                }
                printf("Your guess: ");
                fgets(buff, BUFF_SIZE, stdin);
                guess = strtoul(buff, NULL, 10);
                value = rand();
                if (value == guess) win();
                else puts("Wrong wrong wrong, WRONG!!");
                struct Round *round = malloc(sizeof(struct Round));
                round->guess = guess;
                round->value = value;
                round->number = ++round_number;
                round->next = head;
                head = round;
                break;
            case 3:
                show_stats();
                break;
            case 4:
                if (registered) {
                    unregister_player();
                    puts("Successfully unregistered.");
                    registered = false;
                } else {
                    puts("You're not registered!");
                }
                break;
            default:
                puts("No such option.");
        }
    }

    while (head) {
        struct Round *next = head->next;
        free(head);
        head = next;
    }

    if (round_number == MAX_ROUNDS) puts("You lost too many rounds, cya!");
    else puts("Bye, bye...");
    return 0;
}
