#ifndef ALICHAIN_CLIENT_H_
#define ALICHAIN_CLIENT_H_

namespace alichain {

class Client {
  char name_;

public:
  explicit Client(char name) : name_(name) {}
  int Start(int argc, char* argv[]);
};

}

#endif // ALICHAIN_CLIENT_H_
