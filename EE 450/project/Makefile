CXXFLAGS := -Wall -std=gnu++17 -g

all: serverA

server%: server%.cc backend.h alichain.h
	g++ $(CXXFLAGS) -o $@ $@.cc

tests: tests.cc backend.h
	g++ $(CXXFLAGS) -o $@ $@.cc

clean:
	rm -f serverA

.PHONY: clean
