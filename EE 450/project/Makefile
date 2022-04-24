CXXFLAGS := -Wall -std=gnu++17 -g

all: clientA clientB serverA serverB serverC serverM

client%: client%.cc client.cc
	g++ $(CXXFLAGS) -o $@ $@.cc client.cc

serverM: serverM.cc backend_client.h
	g++ $(CXXFLAGS) -o $@ $@.cc

server%: server%.cc backend.cc
	g++ $(CXXFLAGS) -o $@ $@.cc backend.cc

tests: tests.cc backend.h
	g++ $(CXXFLAGS) -o $@ $@.cc

clean:
	rm -f clientA clientB serverA serverB serverC serverM tests

submission:
	tar -caf ee450_shangnin_1.tar.gz *.cc *.h Makefile README.md

client.cc: alichain.h Socket.h client.h;
backend.h: Socket.h alichain.h;
backend.cc: backend.h;
backend_client.h: Socket.h backend.h alichain.h;

.PHONY: clean submission
