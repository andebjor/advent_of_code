bin:

OPT_FLAGS := -O0
# OPT_FLAGS := -O3

DEBUG_FLAGS := -g

CPPFLAGS := -std=c++14 -W -Wall -Wfatal-errors $(OPT_FLAGS) $(DEBUG_FLAGS)

srcs := solve.cpp circular_list.cpp hasher.cpp
objs := $(patsubst %.cpp, %.o, $(srcs))

prog = solve


bin: $(prog)

solve: $(objs)
	g++ -o $@ $^

%.o: %.cpp
	g++ $(CPPFLAGS) -c -o $@ $<

clean:
	rm -f *.o
	rm -f $(prog)

.PHONY: bin clean
