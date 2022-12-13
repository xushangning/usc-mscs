# Final

## 2020 Fall

### 1

a) No data integrity

- 3: Irrelevant
- 4
- 7: (Irrelevant) Modified HTTP content served by an ARP-spoofing attacker wont't be detected by the firewall.

b) No authentication

- 3
- 4, 7: Irrelevant or wrong

c)

- 6: Compromise of the KDC allows the attacker to steal credentials, but the prof said it was irrelevant.
- ~~8~~: You can definitely do untrusted computation on trusted hardware. However, the problem here is that subversion means another backdoor program is installed, rather than an existing (trusted) program is compromised. When a new backdoor program is installed, maybe it doesn't even have access to files due to the fine-grained access control to persistent resources.
- 5, 7: The question is that if the subversion has happened, are these mechanisms vulnerable? Also, unlike encryption, firewalls and IDS can't prevent 100% of subversion.

d)

- 6: The software that implements Kerberos is definitely exploitable by worms.
- 8: Computing hardware is trusted but the computation itself shouldn't be trusted. This is the only answer prof chose.
- ~~5~~: IDS can detect a worm's anomalous behaviors.

e) 1, 2, 6

f) 6

- ~~5~~: An IDS can flag phishing emails and notify users of failed login attempts.

### 2

1. Attestation is the authentication of computer systems and is implemented by TPM in the following steps:
    1. When each piece of hardware or software is loaded, it will call TPM's extend operation to first, check the current value of PCR to ensure that underlying hardware is not tampered and second, set PCR to the hash value of a combination of the previous PCR and the hardware's own hash.
    2. A computer system will regularly report its attestation status with TPM's quote operation, which signs the current value of PCR with its private endorsement key and reports the signature over network to ensure the integrity of computation.
2. In IPSec, the subject in authentication is the computer, while in HTTPS the subject in authentication is the running web server process. Finally, in authentication performed by an application, only the subject in authentication is the user. (Of course, these differences are fundamentally due to the layers they are operating.)
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

## 2022 Fall

### 1

1. Virtual memory, processes
2. endorsement, storage root key
3. Social engineering
4. ESP, ESP, AH, internet key exchange
5. packet filtering, stateful packet filtering
6. tunnel mode, transport mode
7. virus, trojan horses, worms
8. DNS cache poisoning
9. trusted computing base
10. Traffic analysis
11. vulnerability
12. signature-based detection, anomaly-based detection, network-based detection
13. availability, integrity

### 2

1. Trusted Platform Module (TPM)
    1. “Extend the PCR” means set PCR to the hash value of a combination of the previous PCR value and data that represents the identity of the hardware or software. It is extended before or just after new software (including firmware) like the bootloader or the OS is loaded.
    2. Attestation is possible because the PCR contains a hash chain of the identities of the entire software stack that changes if the identity of any component in the software changes. By using the quote operation to report the signed PCR value and comparing PCR values to known PCR values associated with software stack, we can know the attestation status of the software stack.
    3. It’s impossible to spoof the checksum because first loading is done by the OS protected by address space isolation, over which the subverted software has no control. Secondly, even if the subverted software can control which software to load, it can’t modify the software image that is to be loaded because the image is stored on persistent storage for which the OS implements fine-grained access control to limit access to the image. And finally, even if the subverted software can modify the image, it must create a hash collision ensure that the modified image has the same checksum as the unmodified one, which is computationally difficult for a secure hash function.
2. DNS Security
    1. DNSKEY and DS
    2. The difference is that the chain of trust is DNSSEC corresponds to the hierarchy of domain names, while there is no such correspondence in TLS. Therefore, the certificates for google.com and amazon.com may be signed by different CAs in TLS, while in DNSSEC they must be signed by the same key, “.com” zone’s ZSK. During validation, the certificate chain is followed in TLS while the name hierarchy is followed in DNSSEC.
3. Isolation and Containment
    1. Firewall. Firewall separates different subnets and may be used to separate the domains of public internet and the corporate network.
    2. VPN. VPN provides the separation between the public internet and the corporate network.
    3. Virtual memory. Virtual memory provides isolation for the address space of each process in a computer that prevents for example access to corporate data in a Microsoft Excel from a web browser.
    4. Virtualization technologies. Virtualization technologies provides isolation of an entire operating system and computing resources like memory, persistent storage and even network.

### 3

1. Attacks
    1. Both Approach 1 and 2 are vulnerable to a key logger on a subverted computing device that records the passphrase, optionally copies the key from the thumbdrive to the device, decrypts the private key and uploads it to the attacker’s server.
    2. Approach 2 is also vulnerable to physical theft of the thumb drive combined with offline password cracking of the private key.
    3. Approach 4 is vulnerable to a key logger on a subverted computer that may logs the user’s login credentials.
    4. Approach 4 and 5 are vulnerable to phishing and social engineering attacks, where an attacker may create a fake login website posing as the exchange or call the customer as support staff to request access to the user’s account.
    5. Approach 4 and 5 are also vulnerable to attacks perform by insiders, who may privilege high enough to transfer customer funds.
    6. Approach 5 is vulnerable to the compromise of the exchange’s computer systems, which allows the attacker to use the exchange’s private key to drain customer funds stored in the exchange’s wallet.
2. Defense
    1. The customer and the exchange should keep their systems up to date and apply current patches to reduce the possibility of subversion.
    2. Key theft in approach 1 or 2 can be prevented by using a cold wallet mentioned in Approach 3.
    3. The customer’s device should use trusted computing technologies to attest hardware and software that collects for example biometrics to defend against tampering.
    4. Multi-factor authentication should be used for the exchange in approach 4 and 5, making it more difficult for attackers to obtain both the credentials and the second factor (fingerprint, Yubikeys, OTP).
    5. The exchange should provide regular training to employees (and if possible, customers) to defend against social engineering attacks.
    6. The exchange should implement a containment architecture that separates different classes of data. Specifically, the private keys of the exchange’s wallet  in Approach 5 must reside on a network separate from the corporate network and customer data with firewalls configured to only allow restricted access.
    7. Following the least privilege principle, all employees can be only delegated temporary access to user data only when necessary and the access must be revoked timely.
