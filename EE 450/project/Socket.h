#ifndef ALICHAIN_SOCKET_H_
#define ALICHAIN_SOCKET_H_

#include <iostream>

#include <sys/socket.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <ext/stdio_filebuf.h>

namespace alichain {

/**
 * @brief This class converts socket descriptors to C++ iostream.
 */
class SocketStream {
  // Even though stdio_filebuf accepts the open mode "in | out", we have to
  // create separate filebufs for I/O, because if there is only one filebuf,
  // it will attempt to call lseek(fd, 0, SEEK_CUR) on the socket descriptor
  // during an input operation if that operation is preceded by an output
  // operation.
  __gnu_cxx::stdio_filebuf<char> filebuf_in_, filebuf_out_;

public:
  std::istream in;
  std::ostream out;

  explicit SocketStream(int descriptor) :
    filebuf_in_(descriptor, std::ios_base::in),
    filebuf_out_(descriptor, std::ios_base::out),
    in(&filebuf_in_), out(&filebuf_out_) {}
};

/**
 * @brief A transparent OOP wrapper for Linux sockets (You can intuitively
 * understand the implementation by reading function names.)
 *
 * @details The API assumes that all IP addresses are localhost, so the
 * functions don't have parameters for IP addresses.
 */
class Socket {
private:
  int descriptor_;

public:
  enum class Type : int {
    kTcp = SOCK_STREAM,
    kUdp = SOCK_DGRAM
  };

  int descriptor() const noexcept { return descriptor_; }

  explicit Socket(Type type) {
    descriptor_ = socket(AF_INET, static_cast<int>(type), 0);
    if (descriptor_ == -1)
      throw std::system_error(errno, std::system_category());
  }

  ~Socket() { close(descriptor()); }

  void Bind(uint16_t port) const {
    struct sockaddr_in addr{
      .sin_family = AF_INET,
      .sin_port = htons(port),
      .sin_addr = {inet_addr("127.0.0.1")}
    };
    if (::bind(descriptor(), reinterpret_cast<const struct sockaddr *>(&addr), sizeof(addr)) == -1)
      throw std::system_error(errno, std::system_category());
  }

  void Listen(int backlog) const {
    if (::listen(descriptor(), backlog) == -1)
      throw std::system_error(errno, std::system_category());
  }

  int Accept(uint16_t *client_port = nullptr) const {
    struct sockaddr_in addr;
    socklen_t addrlen = sizeof(addr);
    int connfd = ::accept(descriptor(), reinterpret_cast<struct sockaddr *>(&addr), &addrlen);

    if (client_port)
      *client_port = ntohs(addr.sin_port);

    return connfd;
  }

  void Connect(uint16_t port) const {
    struct sockaddr_in addr{
      .sin_family = AF_INET,
      .sin_port = htons(port),
      .sin_addr = {inet_addr("127.0.0.1")}
    };
    if (::connect(descriptor(), reinterpret_cast<const struct sockaddr *>(&addr), sizeof(addr)) == -1)
      throw std::system_error(errno, std::system_category());
  }

  template <typename T>
  void set_option(int optname, T optval) const {
    if (::setsockopt(descriptor(), SOL_SOCKET, optname, &optval, sizeof(optval)) == -1)
      throw std::system_error(errno, std::system_category());
  }
};

}

#endif // ALICHAIN_SOCKET_H_
