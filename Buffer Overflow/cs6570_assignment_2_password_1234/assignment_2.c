#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void get_name(char *input){
	long canary= 0xD0C0FFEE; 
	char buf[16];
	char out[] = "/bin/sh";
	system("/bin/ls");
	strcpy(buf,input);
	printf("Hi %s!, can you make me run %s ?\n", buf, out);
	if (canary != 0xD0C0FFEE)
		exit(1); 
}

int main(int argc, char **argv){
	if(argc<2)
	{
		printf("Usage:\n%s your_name\n", argv[0]);
		return EXIT_FAILURE;
	}
	get_name(argv[1]);
	return EXIT_SUCCESS;
}


