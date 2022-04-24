#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iomanip>

#include "alichain.h"
#include "Socket.h"
#include "client.h"

namespace alichain {

int Client::Start(int argc, char *argv[]) {
  using std::cout;

  // Parse arguments.
  ServerOperations operation;
  if (argc == 2)
    if (std::string(argv[1]) == "TXLIST")
      operation = ServerOperations::kTxList;
    else
      operation = ServerOperations::kCheckWallet;
  else if (argc == 3 && std::string(argv[2]) == "stats")
    operation = ServerOperations::kStats;
  else if (argc == 4) {
    // Try to parse amount here so that if parsing failed, no data would be
    // sent to the server.
    std::stoi(argv[3]);
    operation = ServerOperations::kTxCoins;
  }
  else {
    std::cerr << "Usage: \n    " << argv[0] << " <username>|TXLIST\n    "
              << argv[0] << " <username1> <username2> <amount>\n";
    return 1;
  }

  Socket sock(Socket::Type::kTcp);
  sock.Connect(kServerPorts[name_ - 'A']);
  cout << "The client " << name_ << " is up and running.\n";

  SocketStream server_stream(sock.descriptor());
  server_stream.in.tie(&server_stream.out);

  server_stream.out << static_cast<int>(operation) << '\n';
  switch (operation) {
    case ServerOperations::kCheckWallet: {
      server_stream.out << argv[1] << '\n';
      cout << '"' << argv[1] << "\" sent a balance enquiry request to the main server.\n";

      int status, balance;
      server_stream.in >> status;
      switch (static_cast<ResponseStatus>(status)) {
        case ResponseStatus::kSuccess:
          server_stream.in >> balance;
          cout << "The current balance of \"" << argv[1] << "\" is : "
               << balance << " alicoins.\n";
          break;
        case ResponseStatus::kUserOrSenderNotFound:
          // https://piazza.com/class/kyll7qbcetu155?cid=164
          cout << "Unable to proceed with the request as \"" << argv[1]
               << "\" is not part of the network.\n";
          break;
        default:
          ;
      }
      break;
    }

    case ServerOperations::kTxCoins: {
      int amount = std::stoi(argv[3]);
      server_stream.out << argv[1] << '\n';
      server_stream.out << argv[2] << '\n';
      server_stream.out << amount << '\n';
      cout << '"' << argv[1] << "\" has requested to transfer " <<
           amount << " coins to \"" << argv[2] << "\".\n";

      int status, balance;
      server_stream.in >> status >> balance;
      server_stream.in.get();
      switch (static_cast<ResponseStatus>(status)) {
        case ResponseStatus::kSuccess:
          cout << '"' << argv[1] << "\" successfully transferred "
               << amount << " alicoins to \"" << argv[2]
               << "\".\nThe current balance of \"" << argv[1] << "\" is : "
               << balance << " alicoins.\n";
          break;
        case ResponseStatus::kInsufficientFunds:
          cout << '"' << argv[1] << "\" was unable to transfer " << amount
               << " alicoins to \"" << argv[2]
               << "\" because of insufficient balance.\nThe current balance of \""
               << argv[1] << "\" is : " << balance << " alicoins.\n";
          break;
        case ResponseStatus::kUserOrSenderNotFound:
          cout << "Unable to proceed with the transaction as \"" << argv[1]
               << "\" is not part of the network.\n";
          break;
        case ResponseStatus::kReceiverNotFound:
          cout << "Unable to proceed with the transaction as \"" << argv[2]
               << "\" is not part of the network.\n";
          break;
        case ResponseStatus::kSenderAndReceiverNotFound:
          cout << "Unable to proceed with the transaction as \"" << argv[1]
               << "\" and \"" << argv[2] << "\" are not part of the network.\n";
          break;
        default:
          ;
      }
      break;
    }

    case ServerOperations::kTxList:
      server_stream.out.flush();
      // https://piazza.com/class/kyll7qbcetu155?cid=274
      cout << "ClientA sent a sorted list request to the main server.\n";
      break;

    case ServerOperations::kStats: {
      server_stream.out << argv[1] << '\n';
      cout << '\"' << argv[1] << "\" sent a statistics enquiry request to the main server.\n";

      int status;
      server_stream.in >> status;
      switch (static_cast<ResponseStatus>(status)) {
        case ResponseStatus::kSuccess: {
          std::size_t n_results;
          server_stream.in >> n_results;
          server_stream.in.get();

          const std::string kHeaders[]{"Rank", "Username", "NumofTransacions", "Total"};
          std::string::size_type widths[]{
            kHeaders[0].size(), kHeaders[1].size(),
            kHeaders[2].size(), kHeaders[3].size()
          };

          struct StatsEntry {
            std::string user_name;
            int n_transactions, amount;
          };
          std::vector<StatsEntry> results(n_results);
          for (std::size_t i = 0; i < n_results; ++i) {
            auto &result = results[i];

            std::getline(server_stream.in, result.user_name);
            server_stream.in >> result.n_transactions >> result.amount;
            server_stream.in.get();

            using std::max;
            using std::to_string;
            widths[0] = max(widths[0], to_string(i + 1).size());
            widths[1] = max(widths[1], result.user_name.size());
            widths[2] = max(widths[2], to_string(result.n_transactions).size());
            widths[3] = max(widths[3], to_string(result.amount).size());

          }
          for (auto &w : widths)
            w = (w / 4 + 1) * 4 - 1;

          using std::setw;
          cout << '\"' << argv[1] << "\" statistics are the following.:\n" << std::left
               << setw(static_cast<int>(widths[0])) << kHeaders[0] << ' '
               << setw(static_cast<int>(widths[1])) << kHeaders[1] << ' '
               << setw(static_cast<int>(widths[2])) << kHeaders[2] << ' '
               << setw(static_cast<int>(widths[3])) << kHeaders[3] << '\n';
          cout << std::right;
          for (std::size_t i = 0; i < n_results; ++i) {
            auto &result = results[i];
            cout << setw(static_cast<int>(widths[0])) << i + 1 << ' '
                 << std::left << setw(static_cast<int>(widths[1])) << result.user_name << ' '
                 << std::right << setw(static_cast<int>(widths[2])) << result.n_transactions << ' '
                 << setw(static_cast<int>(widths[3])) << result.amount << '\n';
          }

          break;
        }

        case ResponseStatus::kUserOrSenderNotFound:
          cout << "Unable to proceed with the request as \"" << argv[1]
               << "\" is not part of the network.\n";
          break;
        default:
          ;
      }

      break;
    }
  }

  return 0;
}

}
