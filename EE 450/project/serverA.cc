#include <vector>

#include "Socket.h"
#include "alichain.h"
#include "backend.h"

int main() {
  alichain::Socket sock(alichain::Socket::Type::kUdp);
  sock.bind(21000 + kUscId3Digits);
  std::cout << "The Server A is up and running using UDP on port "
            << 21000 + kUscId3Digits << ".\n";

  sock.connect(24000 + kUscId3Digits);
  alichain::SocketStream server_stream(sock.descriptor());

  int next_serial_no;
  TransactionLog log(&next_serial_no, "block1.txt");
  server_stream.out << next_serial_no << std::endl;

  while (true) {
    int operation;
    server_stream.in >> operation;
    std::cout << "The ServerA received a request from the Main Server.\n";
    server_stream.in.get();

    switch (static_cast<BackendOperations>(operation)) {
      case BackendOperations::kGetTransactions: {
        std::string name;
        std::getline(server_stream.in, name);
        std::vector<TransactionLog::Transaction> transactions;
        log.GetTransactions(name, transactions);
        server_stream.out << transactions.size() << '\n';
        for (const auto &t : transactions) {
          server_stream.out << t.serial_no << '\n' << t.sender << '\n'
           << t.receiver << '\n' << t.amount << '\n';
        }
        server_stream.out.flush();
        break;
      }
      case BackendOperations::kCreateTransaction: {
        TransactionLog::Transaction t;
        server_stream.in >> t.serial_no;
        server_stream.in.get();
        std::getline(server_stream.in, t.sender);
        std::getline(server_stream.in, t.receiver);
        server_stream.in >> t.amount;
        server_stream.in.get();

        log.CreateTransaction(t);
        server_stream.out << 0 << std::endl;
        break;
      }
      default:
        ;
    }

    std::cout << "The ServerA finished sending the response to the Main Server.\n";
  }

  return 0;
}
