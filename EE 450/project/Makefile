CXXFLAGS := -Wall -std=gnu++17 -g

all: clientA serverA serverM

client%: client%.cc Socket.h
	g++ $(CXXFLAGS) -o $@ $@.cc

serverM: serverM.cc backend_client.h alichain.h
	g++ $(CXXFLAGS) -o $@ $@.cc

server%: server%.cc Socket.h backend.h alichain.h
	g++ $(CXXFLAGS) -o $@ $@.cc

tests: tests.cc backend.h
	g++ $(CXXFLAGS) -o $@ $@.cc

clean:
	rm -f clientA serverA serverM tests

.PHONY: clean
