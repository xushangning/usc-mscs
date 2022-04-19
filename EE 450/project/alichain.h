#ifndef ALICHAIN_H_
#define ALICHAIN_H_

#include <stdint.h>

constexpr uint16_t kUscId3Digits = 761;

enum class BackendOperations {
  kGetTransactions,
  kCreateTransaction
};

#endif // ALICHAIN_H_
