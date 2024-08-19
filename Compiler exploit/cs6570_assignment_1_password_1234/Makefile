FLAGS = -w -m32 -g -fno-stack-protector -z execstack -O0
EXES = shell

default:  clean all
all: $(EXES)
$(EXES):
	gcc $(FLAGS) $@.c -o $@

clean:
	rm -f $(EXES)

