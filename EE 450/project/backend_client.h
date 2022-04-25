#ifndef ALICHAIN_BACKENDCLIENT_H_
#define ALICHAIN_BACKENDCLIENT_H_

#include <iostream>
#include <random>

#include "Socket.h"
#include "backend.h"
#include "alichain.h"

namespace alichain {

class BackendClient {
  using Transaction = TransactionLog::Transaction;

  Socket sock_;
  SocketStream stream_;

  int next_serial_no_ = 1;

public:
  BackendClient(): sock_(Socket::Type::kUdp), stream_(sock_.descriptor()) {
    sock_.Bind(kBackendClientPort);
    stream_.in.tie(&stream_.out);

    // Wait for backends to send their next available serial numbers.
    uint16_t temp;
    for (decltype(kBackendPorts.size()) i = 0; i < kBackendPorts.size(); ++i) {
      stream_.in >> temp;
      stream_.in.get();
      if (next_serial_no_ < temp)
        next_serial_no_ = temp;
    }

    // Set a timeout so that when a backend fails to respond (most likely due to
    // our programming errors), the server won't be forever blocked in recv.
    // This option must be set after next_serial_no_ is obtained. Otherwise, the
    // previous read may fail due to a timeout because the human may start
    // serverA/B/C well after the timeout duration.
    sock_.set_option<struct timeval>(SO_RCVTIMEO, {.tv_sec = 3, .tv_usec = 0});
  }

  void GetTransactions(const std::string &user_name_regex, std::vector<Transaction> &transactions) {
    for (decltype(kBackendPorts.size()) i = 0; i < kBackendPorts.size(); ++i) {
      sock_.Connect(kBackendPorts[i]);

      stream_.out << static_cast<int>(BackendOperations::kGetTransactions)
                  << '\n' << user_name_regex << '\n';
      std::cout << "The main server sent a request to server " << static_cast<char>('A' + i) << ".\n";

      std::size_t n_transactions;
      stream_.in >> n_transactions;
      stream_.in.get();

      for (std::size_t j = 0; j < n_transactions; ++j) {
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
        << static_cast<char>('A' + i) << " using UDP over port "
        << kBackendPorts[i] << ".\n";
    }
  }

  void CreateTransaction(const std::string &sender, const std::string &receiver, int amount) {
    static std::default_random_engine e;
    typedef decltype(kBackendPorts.size()) size_type;
    std::uniform_int_distribution<size_type> d(0, kBackendPorts.size() - 1);
    auto chosen_backend = d(e);

    sock_.Connect(kBackendPorts[chosen_backend]);
    stream_.out << static_cast<int>(BackendOperations::kCreateTransaction)
                << '\n' << next_serial_no_++ << '\n' << sender << '\n' << receiver << '\n'
      << amount << '\n';
    std::cout << "The main server sent a request to server "
      << static_cast<char>('A' + chosen_backend) << ".\n";

    int status;
    stream_.in >> status;
    stream_.in.get();
    std::cout << "The main server received the feedback from server "
      << static_cast<char>('A' + chosen_backend) << " using UDP over port "
      << kBackendPorts[chosen_backend] << ".\n";
  }
};

}

#endif // ALICHAIN_BACKENDCLIENT_H_
