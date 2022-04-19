#include <iostream>
#include <system_error>
#include <vector>

#include <arpa/inet.h>
#include <sys/socket.h>
#include <ext/stdio_filebuf.h>

#include "alichain.h"
#include "backend.h"

int main() {
  int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0)
    throw std::system_error(errno, std::system_category());

  struct sockaddr_in addr{
    .sin_family = AF_INET,
    .sin_port = htons(21000 + kUscId3Digits),
    .sin_addr = {inet_addr("127.0.0.1")}
  };

  if (bind(sockfd, reinterpret_cast<const struct sockaddr *>(&addr), sizeof(addr)) == -1)
    throw std::system_error(errno, std::system_category());

  std::cout << "The Server A is up and running using UDP on port "
            << 21000 + kUscId3Digits << ".\n";

  addr.sin_port = htons(24000 + kUscId3Digits);
  if (connect(sockfd, reinterpret_cast<const struct sockaddr *>(&addr), sizeof(addr)) == -1)
    throw std::system_error(errno, std::system_category());

  __gnu_cxx::stdio_filebuf<char> out_filebuf(sockfd, std::ios_base::out);
  std::ostream server_out(&out_filebuf);
  __gnu_cxx::stdio_filebuf<char> in_filebuf(sockfd, std::ios_base::in);
  std::istream server_in(&in_filebuf);

  TransactionLog log("block1.txt");
  while (true) {
    int operation;
    server_in >> operation;
    std::cout << "The ServerA received a request from the Main Server.\n";
    server_in.get();

    switch (static_cast<BackendOperations>(operation)) {
      case BackendOperations::kGetTransactions: {
        std::string name;
        std::getline(server_in, name);
        std::vector<TransactionLog::Transaction> transactions;
        log.GetTransactions(name, transactions);
        server_out << transactions.size() << '\n';
        for (const auto &t : transactions) {
          server_out << t.serial_no << '\n' << t.sender << '\n'
                     << t.receiver << '\n' << t.amount << '\n';
        }
        server_out.flush();
        break;
      }
      case BackendOperations::kCreateTransaction: {
        TransactionLog::Transaction t;
        server_in >> t.serial_no;
        server_in.get();
        std::getline(server_in, t.sender);
        std::getline(server_in, t.receiver);
        server_in >> t.amount;
        server_in.get();

        log.CreateTransaction(t);
        break;
      }
      default:
        ;
    }

    std::cout << "The ServerA finished sending the response to the Main Server.\n";
  }

  return 0;
}
