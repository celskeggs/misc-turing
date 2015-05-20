#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern int turing_main(void);

int has_eof = 0;

char *load(char *old, int def, unsigned int count, unsigned int tail) {
	old = realloc(old, count);
	if (has_eof) {
		memset(old + count - tail, def, tail);
	} else {
		while (!has_eof && tail) {
			int got = getchar();
			if (got == '\n') { continue; }
			if (got == EOF) { has_eof = 1; break; }
			old[count-tail] = got;
			tail--;
		}
		memset(old + count - tail, def, tail);
	}
	return old;
}

void release(void *ptr, void *end) {
	fwrite(ptr, 1, end - ptr, stdout);
	putchar('\n');
	free(ptr);
}

int main(int argc, char *argv[]) {
	int err = turing_main();
	if (err != -1) {
		fprintf(stderr, "error %d:%d\n", err >> 8, err & 0xFF);
		return 1;
	} else {
		return 0;
	}
}
