CC = gcc
NAME = fn_c_lib.so
SRC = src/c_heuristic/

default: $(NAME)

$(NAME): $(addprefix $(SRC), fn_linear_conflicts.o)
	mkdir -p lib
	$(CC) -dynamiclib $^ -o $(addprefix lib/, $@)

fn_linear_conflicts.o: $(addprefix $(SRC), fn_linear_conflicts.c)
	$(CC) -O3 -fPIC -c $<

clean:
	rm -rf lib
	rm $(addprefix $(SRC), *.o)
