CXXFLAGS := -Wall -std=gnu++17 -g

all: serverA serverM

serverM: serverM.cc backend_client.h alichain.h
	g++ $(CXXFLAGS) -o $@ $@.cc

server%: server%.cc Socket.h backend.h alichain.h
	g++ $(CXXFLAGS) -o $@ $@.cc

tests: tests.cc backend.h
	g++ $(CXXFLAGS) -o $@ $@.cc

clean:
	rm -f serverA serverM tests

.PHONY: clean
