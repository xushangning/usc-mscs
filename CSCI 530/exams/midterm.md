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
