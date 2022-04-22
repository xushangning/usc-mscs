#include <iostream>

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
  sock.connect(kServerPorts[name_ - 'A']);
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
  }

  return 0;
}

}
