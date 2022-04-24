#ifndef ALICHAIN_H_
#define ALICHAIN_H_

#include <array>

#include <stdint.h>

namespace alichain {

constexpr uint16_t kUscId3Digits = 761;

constexpr std::array<uint16_t, 3> kBackendPorts{
  21000 + kUscId3Digits,
  22000 + kUscId3Digits,
  23000 + kUscId3Digits
};
constexpr uint16_t kBackendClientPort = 24000 + kUscId3Digits;

constexpr std::array<uint16_t, 2> kServerPorts{
  25000 + kUscId3Digits,
  26000 + kUscId3Digits
};

enum class BackendOperations {
  kGetTransactions,
  kCreateTransaction
};

enum class ServerOperations {
  kCheckWallet,
  kTxCoins,
  kTxList
};

enum class ResponseStatus {
  kSuccess,
  kUserOrSenderNotFound,
  kReceiverNotFound,
  kSenderAndReceiverNotFound,
  kInsufficientFunds
};

}

#endif // ALICHAIN_H_
