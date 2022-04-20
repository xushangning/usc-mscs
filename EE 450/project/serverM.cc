#include <iostream>
#include <string>

#include "alichain.h"
#include "backend_client.h"

using std::string;
using std::vector;

using Transaction = TransactionLog::Transaction;

int CalculateBalance(const string &name, vector<Transaction> &transactions) {
  int balance = 1000;
  for (const auto &t: transactions)
    balance += t.receiver == name ? t.amount : - t.amount;
  return balance;
}

int main() {
  using std::cout;
  using std::getline;

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
        string name;
        getline(client_stream.in, name);
        cout << "The main server received input=\"" << name
          << "\" from the client using TCP over port " << client_port << ".\n";

        vector<Transaction> transactions;
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

      case ServerOperations::kTxCoins: {
        string sender, receiver;
        int amount;
        getline(client_stream.in, sender);
        getline(client_stream.in, receiver);
        client_stream.in >> amount;
        client_stream.in.get();
        cout << "The main server received from \"" << sender << "\" to transfer "
          << amount << " coins to \"" << receiver
          << "\" using TCP over port " << client_port << ".\n";

        ResponseStatus status = ResponseStatus::kSuccess;
        vector<Transaction> transactions;
        backend_client.GetTransactions(receiver, transactions);
        if (transactions.empty())
          status = ResponseStatus::kReceiverNotFound;
        else
          transactions.clear();
        backend_client.GetTransactions(sender, transactions);
        if (transactions.empty())
          status = status == ResponseStatus::kReceiverNotFound ?
            ResponseStatus::kSenderAndReceiverNotFound :
            ResponseStatus::kUserOrSenderNotFound;
        if (status != ResponseStatus::kSuccess) {
          client_stream.out << static_cast<int>(status) << std::endl;
          break;
        }

        int balance = CalculateBalance(sender, transactions);
        if (balance < amount) {
          status = ResponseStatus::kInsufficientFunds;
          client_stream.out << static_cast<int>(status) << std::endl;
          break;
        }

        backend_client.CreateTransaction(sender, receiver, amount);
        client_stream.out << static_cast<int>(status) << '\n'
          << balance - amount << std::endl;
        cout << "The main server sent the result of the transaction to client A.\n";
        break;
      }

      default:
        ;
    }
  }
}
