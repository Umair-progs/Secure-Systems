#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <signal.h>

#define BOLD_GREEN "\x1b[1;32m"
#define RESET      "\x1b[0m"

#define NAME_LEN  12
#define TOKEN_LEN 16
#define SIZE      13

const char *BANNER =
	"  _____ ____   _____ _______ ___  _  __\n"
	" / ____|___ \\ / ____|__   __/ _ \\| |/ /\n"
	"| (___   __) | |       | | | | | | ' / \n"
	" \\___ \\ |__ <| |       | | | | | |  <  \n"
	" ____) |___) | |____   | | | |_| | . \\ \n"
	"|_____/|____/ \\_____|  |_|  \\___/|_|\\_\\\n";

typedef struct struct_token_t {
	char *token;
	bool occupied;
} token_t;

static token_t tokens[SIZE];

void strip_newline(char *str) {
	char *null_pos = strchr(str, '\n');
	if (null_pos) {
		*null_pos = '\0';
	} else {
		return;
	}
}

void introduce() {
	char name[NAME_LEN];

	printf("What is your 4-letter name? ");

	fgets(name, NAME_LEN, stdin);
	strip_newline(name);

	printf("Hi ");
	printf(name);
	printf("! I will be generating tokens for you.\n");
}

void gentok() {
	for (int i = 0; i < SIZE; i++) {
		if (!tokens[i].occupied) {
			char *token = malloc(TOKEN_LEN);
			printf("Enter the name for the token: ");

			fgets(token, TOKEN_LEN, stdin);
			strip_newline(token);

			tokens[i].token = token;
			tokens[i].occupied = true;
			break;
		}
	}
}

void distok() {
	char input_token[3];

	printf("Enter the index of the token: ");
	fgets(input_token, 3, stdin);
	strip_newline(input_token);

	int token_id = atoi(input_token);
	free(tokens[token_id].token);
	tokens[token_id].occupied = false;
}

void printtok() {
	for (int i = 0; i < SIZE; i++) {
		if (tokens[i].occupied) {
			printf("%d: %s\n", i, tokens[i].token);
		}
	}
}

void binsh() {
	execve("/bin/sh", NULL, NULL);
}

/* --- IGNORE --- */
void timeout_kill(int sig) {
	if (sig == SIGALRM) {
		printf("[!] Timed out.");
		_exit(0);
	}
}

void init_signal() {
	signal(SIGALRM, timeout_kill);
	alarm(60);
}

void init_buffering() {
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
}
/* --- IGNORE --- */

int main(int argc, char *argv[]) {
	/* --- IGNORE --- */
	init_signal();
	init_buffering();
	/* --- IGNORE --- */

	printf(BOLD_GREEN "%s\n\n" RESET, BANNER);

	for (int i = 0; i < SIZE; i++) {
		tokens[i].token = NULL;
		tokens[i].occupied = false;
	}

	introduce();

	char c;
	while (1) {
		printf("\n==================\n");
		printf("What can I do for you?\n");
		printf("  - [g]enerate a new token\n");
		printf("  - [d]iscard an existing token\n");
		printf("  - [p]rint all your tokens\n");
		printf("  - e[x]it the program\n");
		printf("Action: ");

		c = fgetc(stdin);
		fgetc(stdin); // consume newline

		switch (c) {
		case 'g':
			gentok();
			break;
		case 'd':
			distok();
			break;
		case 'p':
			printtok();
			break;
		case 'x':
			goto end;
		default:
			printf("Invalid command!\n");
		}
	}

end:
	printf("Goodbye\n");
	return 0;
}
