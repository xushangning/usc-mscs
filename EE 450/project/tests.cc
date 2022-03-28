#define CATCH_CONFIG_MAIN
#include <catch2/catch.hpp>

#include "backend.h"

TEST_CASE("Load transactions from file and filter transactions", "[TransactionLog]") {
  TransactionLog log("block1.txt");
  std::vector<TransactionLog::Transaction> transactions;
  log.GetTransactions(".+", transactions);
  REQUIRE(transactions.size() == 3);

  transactions.clear();
  log.GetTransactions("John", transactions);
  const auto &t = transactions[0];
  REQUIRE(t.serial_no == 1);
  REQUIRE(t.sender == "Racheal");
  REQUIRE(t.receiver == "John");
  REQUIRE(t.amount == 45);
}
