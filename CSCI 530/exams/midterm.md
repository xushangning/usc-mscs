# Midterm

## Fall 2017

### 1

1. 6, 7
2. 3, 5, 6
3. 1, 2, 4, 5, 7
4. 1, 2, 3, 4, 5, 7
5. 3, 6, 7
6. 1, 4

### 2

1. In Bell-Lapadula, a subject can only write up (produce data with a more confidential label) and read down (read data less than or equal to its clearance) to protect confidentiality of objects, while in Biba a subject can only write down and read up to ensure that data at a higher classification level cannot be modified by subjects with lower clearance.
2. Authentication
    1. Something you know
        1. Example: passwords, cryptographic keys
        2. Advantages or disadvantages
            1. Remembering things is hard for humans, which leads to password reuse or writing down passwords on a post-it note or on the white board that are easy to steal.
            2. Coming up with a difficult-to-guess but easy-to-remember password is in itself difficult. People frequently use information that are not known exclusively to themselves as passwords, which are easy to guess.
    2. Something you have
        1. Examples: badge, card
        2. Advantages or disadvantages
            1. The security of the thing you have may be weak e.g., mag stripes and easy to duplicate.
            2. Devices like RSA SecureID Tokens relies on seeds stored centrally on RSA company's servers that may be compromised by hackers.
    3. Something about you
        1. Examples: fingerprints, iris
        2. Advantages or disadvantages
            1. Not suitable when the collection device can't be trusted.
            2. Can be duplicate.
3. Bell-Lapadula only allows information to flow into more secure compartments: a subject can only produce data that are at least classified as its clearance and can only read data with lower security classification. It prevents information disclosure information is never read by people with lower clearance but is useless with regard to system compromise as it can only read less classified and thus trusted information. On the contrary, Biba is a pretty good defense against system compromise but not for information disclosure.

### 3

1. The existing form of authentication involves asking the applicant for they know like name, date of birth and social security numbers, which are not really confidential. These kinds of personal information are exactly the ones leaked during the Equifax breach, leading to potential identity theft.
2. Improving the situation
    1. Instead of asking new users for personal information, we can use federated identity solution like Shibboleth that asks new users to provide their identities through other identity providers like Equifax.
    2. The advantages are that compared with passwords, personal information is easier to be abused by hackers in a data breach because it is stored in plaintext. Also, one fewer opportunity of typing your personal information for enrollment reduces the possibility of information leak e.g., by people glancing at your computer screen or by keyboard logger. Even if your personal information is stolen in a breach, they can't be used to apply for credit cards if the credit card company only allows federated identity.
    3. Our approach depends on the identity provider for security, which as the Equifax breach shows may still have security problems. Other problems the identity provide may have are that it may also depend on personal information enrollment at the identity provider, or its employees are susceptible to social engineering and phishing.
    4. Our approach doesn't apply to users who don't have an identity with other identity providers that have necessary information for credit card application.
    5. A criminal may be able to apply for credit cards through means that are still authenticated by personal information, like through mail or phone call, or even through social engineering trick customer support for credit card companies to issue a replacement card for an existing one.
    6. We can require people who want to authenticate with personal information to apply at a local branch with the credit card company.
3. The company should establishes data access policies with Bell-Lapadula and Biba. Customer personal information and employee credentials should have the top security classification to limit the number of subjects that can access them. Internet-facing web servers should have the lowest integrity level, followed by company-issued devices at a higher integrity level. Subjects at different integrity levels should be compartmented in internal networks to limit the scope of security compromise (if any).

## Fall 2021

### 1

Mechanism | Client Auth | Server Auth | Information Held Client | Information Held Server | Third Party | Keys held at end
--- | --- | --- | --- | --- | --- | ---
Kerberos | Yes | Yes | Kc | Ks | KDC, TGS | Session key
Diffie-Hellman | No | No | NA | NA | None | $g^{xy}$
SSL or TLS (server cert only) | No | Yes | NA | Server cert | None | 4 session keys for confidentiality and integrity
SSH | Yes | Yes | Password or client public key | Server public key | None | None
PGP or GPG | Yes | Yes | Client public key | Server public key | Directory service | None

## Fall 2022

### 1

a) 4, 6

- ~~1~~: Considered a minor characteristic because although the security classification assigned to each object is associated with objects, the policy itself is not associated with objects.

b) 5

c) 1

d) 2

e) 1, 2

f) 1 (minor), 3, 6

g) 5

### 2

1. Expiration date
    1. Because as time passes, there is growing probability that the issued certificate or ticket is compromised e.g., brute-forced and no longer valid. The expiration date also ensures that if the key is stolen or guessed or brute-forced, the adversary won't be able to impersonate you using the compromised key indefinitely.
    2. A longer lifetime adds to the ease of use for users and reduces burden on the revocation mechanism, when there are fewer certificates that need to be revoked. A shorter lifetime gives high assurance on the validity of credentials.
    3. Because in Kerberos there is a trusted third-party KDC that handles the revocation.
2. Nonce and timestamp
    1. They defend against replay attacks and ace used in authentication in public key cryptography.
    2. Timestamps are easier to generate than nonces but require a synchronized clock. Nonces simplify the protocol because when timestamps are used, the validator must accept a range of timestamps, instead of a single value like nonce due to impreciseness of clocks. The range of acceptable timestamps is the time window in which messages can be replayed, so additional mechanism must be designed to defend against replay attacks.
3. Because during authentication with mag stripe cards, the card reader can read the complete key from the card, unlike other physical devices like Yubikeys, making the stripe cards easy to be replicated. Just like attacks on passwords, once an adversary gets a copy of your stripe card key, they don’t need the original physical card anymore and can “replay” just the key.
4. The public key is obtained from the list of trusted CA stored in the browser. If we had an incorrect public key for the CA, the connection would fail because the browser couldn’t validate the certificate provided by the server. If we accepted the public key of CA not worthy of our trust, when combined with a man-in-the middle attack, the CA issuer might be able to decrypt the connection and read the communication.
5. Intermediate transmission infrastructure may enable man-in-the-middle attacks, where the infrastructure participates in key exchange and offer its own key to the communication parties. The implication is that the infrastructure will be able to read all the communication in between or to impersonate people in Whatsapp and ask for your credentials or requset money transfer.

### 3

1. General Approach of the attack
    1. Administrators in LAUSD may not use multi-factor authentication. The adversary can reuse passwords from past breaches and to try to log into computer systems. After they logged in, they will be able to modify the system and install ransomware.
    2. A public facing LAUSD website that is just set up may lack TLS. When a teacher or an administrator logs into the website on public Wi-Fi network and is observed by the adversary, they may be able eavesdrop on the connection and steal the credentials. With credentials, they can scout for information on the website used for phishing attacks.
    3. Due to misconfiguration on the firewall, an unguarded internal computer is exposed to the internet that should have been limited to internal network. The adversary found the computer by scanning the LAUSD’s IP rang, use the computer to hop into the internal network and install the ransomware on the computer.
2. Policy and access control
    1. Least privilege
    2. Role-based access models
    3. The Biba model should also be implemented here to safeguard the integrity of computer systems. Data produced by different computer systems should have different integrity levels. For example, data stored and produced by public-facing servers and LAUSD-issued laptops should have the lowest integrity level. Systems with higher integrity levels should only be able to write to, but not read from public-facing servers. Systems in the internal network should have a higher integrity level and systems directly managed by the incident response team should have the highest integrity level. In this way, if only the
3. Authentication
    1. A federated identity solution like Shibboleth should be deployed across LAUSD to enable single sign-on for computer systems to reduce the possibility of a breach in a weak credential management system.
    2. Multi-factor authentication should be enabled across all users. Students, parents and even teachers may only need SMS-based or Duo-based authentication on their phone. District and school administrators should carry physical devices like Yubikeys for enhanced security.
    3. Access to computer systems, including laptops, workstations, websites and even Wi-Fi networks should go through an authentication protocol like Kerberos to ensure the trustworthiness of access.
