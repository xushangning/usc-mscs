# EE450 Socket Programming Project, Spring 2022

Shangning Xu 3010562761

1. Scope of the project: All operations (including the bonus stats operation) have been completed.
2. Source files (only files not explicitly required by the handout are described):
    1. alicahin.h: declarations that are useful for the entire project e.g., port numbers
    2. backend.h, backend.cc: the backend server
    3. backend_client.h: client to the backend server used by Server M
    4. client.h, client.cc: the client to Server M
    5. Socket.h: a wrapper for Berkeley Socket API
    6. tests.cc: test cases
3. Message format: All messages are plain text on a request-response basis.
    1. Request: `<operation>\n[<arg>\n]*`
    2. Response: `<response-status>\n[<return-value>\n]*`
4. Idiosyncrasies: When partial data transfer happens e.g., when the client only sends half of the message before being killed by the user, the server will be stuck forever waiting for the remaining data, because no timer is set (except for a few places) and all programs are single-threaded.
5. Reused code: All code is written from scratch.
6. References and acknowledgements
    1. *Computer Systems: A Programmer's Perspective, 3rd Edition*: This is what get me started with socket programming (and system programming in general) during undergrad.
    2. *The Linux Programming Interface* by Micheal Kerrisk: An excellent reference for the Linux programming interface, including the socket interface. I'm fortunate to come upon this book when I was preparing for an interview.
