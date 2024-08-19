FLAGS = -m32 -static -g -fno-stack-protector -O0 
EXES = assignment_2

default:  clean all
all: $(EXES)
$(EXES):
	gcc $(FLAGS) $@.c -o $@

clean:
	rm -f $(EXES)

