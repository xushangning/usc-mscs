#ifndef ALICHAIN_BACKENDCLIENT_H_
#define ALICHAIN_BACKENDCLIENT_H_

#include <iostream>

#include "Socket.h"
#include "backend.h"
#include "alichain.h"

namespace alichain {

class BackendClient {
  using Transaction = TransactionLog::Transaction;

  Socket sock_;
  SocketStream stream_;

public:
  BackendClient(): sock_(SOCK_DGRAM), stream_(sock_.descriptor()) {
    // Set a timeout so that when a backend fails to respond (most likely due to
    // our programming errors), the server won't be forever blocked in recv.
    sock_.set_option<struct timeval>(SO_RCVTIMEO, {.tv_sec = 3, .tv_usec = 0});
    sock_.bind(24000 + kUscId3Digits);
    stream_.in.tie(&stream_.out);
  }

  void GetTransactions(const std::string &user_name_regex, std::vector<Transaction> &transactions) {
    sock_.connect(21000 + kUscId3Digits);

    stream_.out << static_cast<int>(BackendOperations::kGetTransactions)
      << '\n' << user_name_regex << '\n';
    std::cout << "The main server sent a request to server A.\n";

    std::size_t n_transactions;
    stream_.in >> n_transactions;
    stream_.in.get();

    for (std::size_t i = 0; i < n_transactions; ++i) {
      Transaction t;

      stream_.in >> t.serial_no;
      stream_.in.get();

      std::getline(stream_.in, t.sender);
      std::getline(stream_.in, t.receiver);

      stream_.in >> t.amount;
      stream_.in.get();

      transactions.push_back(t);
    }
    std::cout << "The main server received transactions from Server "
                 "A using UDP over port "
      << 21000 + kUscId3Digits << ".\n";
  }
};

}

#endif // ALICHAIN_BACKENDCLIENT_H_
