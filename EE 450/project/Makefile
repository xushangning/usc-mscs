CXXFLAGS := -Wall -std=gnu++17 -g

all: clientA clientB serverA serverB serverC serverM

client%: client%.cc client.cc client.h
	g++ $(CXXFLAGS) -o $@ $@.cc client.cc

serverM: serverM.cc backend_client.h alichain.h
	g++ $(CXXFLAGS) -o $@ $@.cc

server%: server%.cc backend.cc backend.h
	g++ $(CXXFLAGS) -o $@ $@.cc backend.cc

tests: tests.cc backend.h
	g++ $(CXXFLAGS) -o $@ $@.cc

clean:
	rm -f clientA clientB serverA serverB serverC serverM tests

.PHONY: clean
