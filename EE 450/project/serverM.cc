#include <iostream>
#include <string>

#include "alichain.h"
#include "backend_client.h"

int main() {
  using std::cout;

  alichain::Socket server(SOCK_STREAM);
  server.set_option(SO_REUSEADDR, 1);
  server.bind(25000 + kUscId3Digits);
  server.listen(1024);

  alichain::BackendClient backend_client;

  cout << "The main server is up and running.\n";

  while (true) {
    uint16_t client_port;
    int connfd = server.accept(&client_port);
    if (connfd == -1)
      continue;

    alichain::SocketStream client_stream(connfd);
    client_stream.in.tie(&client_stream.out);

    int operation;
    client_stream.in >> operation;
    client_stream.in.get();
    switch (static_cast<ServerOperations>(operation)) {
      case ServerOperations::kCheckWallet: {
        std::string name;
        std::getline(client_stream.in, name);
        cout << "The main server received input=\"" << name
          << "\" from the client using TCP over port " << client_port << ".\n";

        std::vector<TransactionLog::Transaction> transactions;
        backend_client.GetTransactions(name, transactions);

        if (transactions.empty()) {
          client_stream.out
            << static_cast<int>(ResponseStatus::kUserOrSenderNotFound)
            << std::endl;
          break;
        }

        int balance = 1000;
        for (const auto &t: transactions)
          balance += t.receiver == name ? t.amount : - t.amount;
        client_stream.out << static_cast<int>(ResponseStatus::kSuccess) << '\n'
          << balance << std::endl;
        cout << "The main server sent the current balance to client A.\n";
        break;
      }
      default:
        ;
    }
  }
}
