# CSCI 531 Programming Assignment 1 Design Document

The purpose of the system is to provide a correct and tested implementation of the AES-128 encryption scheme in the ECB mode. The main design goal of our AES implementation is correctness of encryption and decryption.

Our AES implementation consists of three parts: the AES-128 encryption algorithm, the AES-128 decryption algorithm, and a test script that demonstrates the correctness of our AES implementation. All scripts in our implementation are runnable on a computer with Python 3 installed and the NumPy package. NumPy is used in our AES implementation for the following reasons:

- It supports the fixed-size integer types `uint8`. Byte manipulation is more natural with `uint8` than Python `int` which has unlimited precision.
- It supports a variety of (sometimes vectorized) operations on multi-dimensional arrays like matrix multiplication and element-wise arithmetic that are faster and less error-prone than our own implementation.

AES-128 constants are defined in the implementation for the encryption algorithm and are depended on by the decryption algorithm and the test script. The test script depends on both the AES-128 encryption and decryption algorithm to work.

All three parts of our AES implementation are implemented as Python 3 scripts (`aesencrypt.py`, `aesdecrypt.py` and `aestest.py`) and are designed to run from the command line. The first two files have required command-line arguments and print out results or error messages and exit. Help messages can be obtained with the `-h` flag. `aestest.py` only accepts user input from the standard input and additionally contains unit tests that can be run individually or in bulk to further demonstrate the correctness of various parts of the AES-128 implementation.

The padding scheme for our encryption scheme implementation is ISO/IEC 7816-4.

`aesencrypt.py` has only one error condition, when the key is not 16-byte long. `aesdecrypt.py` has the key length error condition and reports the invalid padding error when the padding format is incorrect. `aestest.py` has no error conditions.

## Notes on AES-128 Implementation

AES transformations are implemented on top of NumPy operations. `SubBytes` and its inverse are implemented using NumPy indexing operator to index into a look-up table that contains 256 bytes:

```python
# state is the AES internal state and S_BOX is the substitution table. Both are
# NumPy arrays.
state = S_BOX[state]
```

`ShiftRows` (and its inverse) and `RotWords` are implemented with `numpy.roll`. `MixColumns` and its inverse are implemented as matrix multiplication under GF(2^8) according to equations (5.6) and (5.10) in the AES Standard. The function `galois_field_2_to_8th_mul` for scalar multiplication under GF(2^8) is implemented according to the algorithm outlined in Section 4.2.1 in the AES Standard, and matrix multiplication `galois_field_2_to_8th_mat_mul` is based on scalar multiplication.

An important difference between our implementation and the algorithm given in the standard is that in the standard bytes are arranged in the column-major order but in our implementation in row-major order, which is the convention of NumPy. Therefore, order of matrices in matrix multiplication must be reversed compared with the algorithm in the standard. Consider equation (5.6) and our implementation for it:

```python
# Equation (5.6)
state = galois_field_2_to_8th_mat_mul(
    MIX_COLUMNS_COEFFICIENT, state
)
# Our implementation
state_transposed = galois_field_2_to_8th_mat_mul(
    state_transposed, MIX_COLUMNS_COEFFICIENT_TRANSPOSED
)
```

## Demo

For better readability, the text for the terminal session when `aestest.py` was run is reproduced below instead of a screenshot.

```
> python3 aestest.py
Please enter a one-line message to encrypt: The quick brown fox jumps over the lazy dog.
The randomly generated key is 5bf876bf40199ea4c1b554822c31b1e9.
The ciphertext: d3a27889932ff24229d4fc92c30737f63e94d9e6b97215f50a7d387bfa5de583f05dcbe3cfe473434507cbae7f9b76f6
The decrypted plaintext: The quick brown fox jumps over the lazy dog.
```

## Reference

*Specification for the Advanced Encryption Standard (AES)*. 2001, http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf.
