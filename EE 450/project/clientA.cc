#include "client.h"

int main(int argc, char* argv[]) {
  alichain::Client c('A');
  c.Start(argc, argv);

  return 0;
}
