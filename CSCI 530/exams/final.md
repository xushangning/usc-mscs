# Final

## 2020 Fall

### 1

a) No data authentication

3, 4

- 7: Modified HTTP content served by an ARP-spoofing attacker wont't be detected by the firewall.

b) No key authentication

3, 4, 7

c)

- 6: Compromise of the KDC allows the attacker to steal credentials.
- 8: You can definitely do untrusted computation on trusted hardware.
- ~~5~~: An IDS can detect privilege escalation of programs that normally shouldn't have privilege.
- ~~7~~: The firewall can inspect a packet's payload and match it against existing rules to ensure that services running on the computer won't be exploited.

d)

- 6: The software that implements Kerberos is definitely exploitable by worms.
- 8: Computing hardware is trusted but the computation itself shouldn't be trusted.
- ~~5~~: IDS can detect a worm's anomalous behaviors.

e) 1, 2, 3, 5, 6, 7, 8

f) 1, 6, 7

- ~~5~~: An IDS can flag phishing emails and notify users of failed login attempts.

### 2

1. Attestation is the authentication of computer systems and is implemented by TPM in the following steps:
    1. When each piece of hardware or software is loaded, it will call TPM's extend operation to first, check the current value of PCR to ensure that underlying hardware is not tampered and second, set PCR to the hash value of a combination of the previous PCR and the hardware's own hash.
    2. A computer system will regularly report its attestation status with TPM's quote operation, which signs the current value of PCR with its private endorsement key and reports the signature over network to ensure the integrity of computation.
2. In IPSec, both the client and the server are authenticated, while in HTTPS only the server is authenticated. Finally, in authentication performed by an application, only the client is authenticated.
3. The zones in DNSSEC corresponds to CAs in TLS and the combination of zone signing keys and key signing keys correspond to certificates in TLS. Like the PKI of TLS, DNSSEC also establishes a hierarchy of zones where the parent zone signs the child zone's ZSK with its own ZSK, while resource records in a zone are signed by KSK, which are in turn signed by ZSK of that zone.
4. Here are the advantages of a network-based IDS:
    - Network-based intrusion detection systems provide higher availability and are more resilient because failure in one IDS doesn't affect the operation of others, while a monolithic IDS is a single point of failure in the entire system.
    - Network-based IDSs have access to more data sources than a monolithic system sitting on one end system, which allows network-based IDSs to for example to detect intrusion earlier and to create a more complete picture of ongoing intrusion.
    - Some attacks like DDoS are inherently distributed and may not be detected by a monolithic IDS until very late stage into the attack, while network-based IDSs have presence in multiple places in the network and can respond to attack early.

### 3

1. Containment
    1. The boundaries of the protection domain for corporate data extend to offer protection for communication between work computers and corporate network over the public internet, because employees need to access corporate data at home. Previously, the protection domain only needs to include the corporate network because work computers are directly attached to the corporate network without going through the internet.
    2. Prior to the pandemic firewalls are used to provide isolation / separation of protection domains, while VPNs see increased use during the pandemic.
    3. The company should restrict access to the corporate network to employees that are using VPN. Firewalls of work computer should be configured to restrict the level of access similar to the firewall that protects the corporate network, at least during working hours.
2. Here are the difficulties for a corporate intrusion detection system:
    - The IDS is unable to detect intrusion from a (compromised) home network to which a work computer is attached, if parts of the IDS are not installed on the computer.
    - Work-from-home changes the network traffic pattern inside the corporate network e.g., more traffic now comes from exit points of VPN inside the corporate network, where few IDS are previously installed or they are slow to respond due to sheer amount of traffic. The changed access patterns also mean that previously configured criteria for intrusion may no longer work and lead to more false positives.
3. Trusted computing
    1. Trusted computing can be used in the following ways:
        1. Software like OS login, VPN client and Excel that handles important data (credentials and customer data) should verify the attestation of the operating system and the boot loader to ensure that they are not tampered with and that the OS is up-to-date and refuse to launch if otherwise.
        2. The company should monitor attestation status of reported by TPMs of work computers and resolve non-compliance issues timely.
        3. Work computers should implement full disk encryption where disk data can only be decrypted when PCR is set to specific values, which prevent data leaks due to theft of work computers.
        4. The OS should support fine-grained access control for persistent resources like files and enforce separation of address space between processes so that untrusted applications and malware can't access critical data.
    2. Subverted applications can't access corporate information because the OS enforces separation of address space of processes and fine-grained access control on persistent resources. With the protection, subverted applications can access neither the memory or persistent storage used by processes that handle corporate data.
