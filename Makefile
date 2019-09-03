CC = gcc
NAME = fn_c_lib.so
SRC = src/c_heuristic/

default: $(NAME)

$(NAME): $(addprefix $(SRC), fn_linear_conflicts.o)
	@mkdir -p lib
	@$(CC) -dynamiclib $^ -o $(addprefix lib/, $@)
	@printf "\e[32;1mcreated:\e[0m %s\n" $(NAME)

fn_linear_conflicts.o: $(addprefix $(SRC), fn_linear_conflicts.c)
	@$(CC) -O3 -fPIC -c $<

clean:
	@rm -rf lib
	@rm -f $(addprefix $(SRC), *.o)
	@printf "\e[31;1mcleaning..\e[0m\n"
