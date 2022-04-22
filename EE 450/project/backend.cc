#include "backend.h"

namespace alichain {

void Backend::Start() {
  sock_.bind(port_);
  std::cout << "The Server" << name_
    << " is up and running using UDP on port " << port_ << ".\n";

  sock_.connect(kBackendClientPort);
  SocketStream server_stream(sock_.descriptor());

  int next_serial_no;
  TransactionLog log(
    &next_serial_no,
    std::string("block") + std::to_string(name_ - 'A' + 1) + ".txt"
  );
  server_stream.out << next_serial_no << std::endl;

  while (true) {
    int operation;
    server_stream.in >> operation;
    std::cout << "The Server" << name_ << " received a request from the Main Server.\n";
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

    std::cout << "The Server" << name_ << " finished sending the response to the Main Server.\n";
  }

}

}
