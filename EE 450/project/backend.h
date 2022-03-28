#ifndef BACKEND_H_
#define BACKEND_H_

#include <string>
#include <vector>
#include <fstream>
#include <string_view>

class TransactionLog {
public:
  struct Transaction {
    int serial_no;
    std::string sender, receiver;
    int amount;
  };

private:
  std::vector<Transaction> log;

public:
  explicit TransactionLog(const std::string_view &block_file = {}) {
    if (block_file.empty())
      return;

    using std::ifstream;
    ifstream block_fin(block_file.data());
    if (!block_fin.is_open())
      throw std::system_error(errno, std::system_category());

    Transaction t;
    while (block_fin >> t.serial_no >> t.sender >> t.receiver >> t.amount)
      log.push_back(t);
  }

  void GetTransactions(const std::string_view &user_name_regex, std::vector<Transaction> &transactions) {
    if (user_name_regex == ".+") {
      transactions = log;
      return;
    }

    for (auto &t : log)
      if (t.sender == user_name_regex || t.receiver == user_name_regex)
        transactions.push_back(t);
  }
};

#endif // BACKEND_H_
