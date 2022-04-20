#ifndef BACKEND_H_
#define BACKEND_H_

#include <string>
#include <vector>
#include <fstream>
#include <cassert>

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
  explicit TransactionLog(int *next_serial_no, const std::string &block_file = {}) {
    assert(next_serial_no);
    *next_serial_no = 1;
    if (block_file.empty())
      return;

    using std::ifstream;
    ifstream block_fin(block_file.data());
    if (!block_fin.is_open())
      throw std::system_error(errno, std::system_category());

    Transaction t;
    int max_serial_no = 0;
    while (block_fin >> t.serial_no >> t.sender >> t.receiver >> t.amount) {
      if (max_serial_no < t.serial_no)
        max_serial_no = t.serial_no;
      log.push_back(t);
    }
    *next_serial_no = max_serial_no + 1;
  }

  void GetTransactions(const std::string &user_name_regex, std::vector<Transaction> &transactions) {
    if (user_name_regex == ".+") {
      transactions = log;
      return;
    }

    for (auto &t : log)
      if (t.sender == user_name_regex || t.receiver == user_name_regex)
        transactions.push_back(t);
  }

  void CreateTransaction(const Transaction &t) { log.push_back(t); }
};

#endif // BACKEND_H_
