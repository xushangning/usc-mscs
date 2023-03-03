from unittest import TestCase
from secrets import token_hex
import subprocess

import numpy as np

from aesencrypt import (
    expand, galois_field_2_to_8th_mul, galois_field_2_to_8th_mat_mul,
    MIX_COLUMNS_COEFFICIENTS, encrypt, KEY_SIZE
)
from aesdecrypt import decrypt


class TestAES(TestCase):
    KEY = np.array(
        (
            (0x2b, 0x7e, 0x15, 0x16), (0x28, 0xae, 0xd2, 0xa6),
            (0xab, 0xf7, 0x15, 0x88), (0x09, 0xcf, 0x4f, 0x3c)
        ),
        dtype=np.uint8
    )
    """Example 128-bit key from the AES Standard (FIPS 197)"""

    def test_expand(self):
        schedule = expand(self.KEY)
        # Examples selected from Appendix A.2 of the AES Standard
        self.assertEqual(0x2b, schedule[0][0])
        self.assertEqual(0xc2, schedule[8][1])
        self.assertEqual(0xad, schedule[19][2])
        self.assertEqual(0x21, schedule[32][3])
        self.assertEqual(0xb6, schedule[43][0])

    def test_galois_field_2_to_8th_mul(self):
        self.assertEqual(0xc1, galois_field_2_to_8th_mul(np.uint8(0x57), np.uint8(0x83)))
        self.assertEqual(0xfe, galois_field_2_to_8th_mul(np.uint8(0x57), np.uint8(0x13)))

    def test_galois_field_2_to_8th_mat_mul(self):
        expected = np.array(
            (
                (0x04, 0x66, 0x81, 0xe5),
                (0xe0, 0xcb, 0x19, 0x9a),
                (0x48, 0xf8, 0xd3, 0x7a),
                (0x28, 0x06, 0x26, 0x4c)
            ),
            dtype=np.uint8
        )
        result = galois_field_2_to_8th_mat_mul(
            np.array(
                (
                    (0xd4, 0xbf, 0x5d, 0x30),
                    (0xe0, 0xb4, 0x52, 0xae),
                    (0xb8, 0x41, 0x11, 0xf1),
                    (0x1e, 0x27, 0x98, 0xe5)
                ),
                dtype=np.uint8
            ),
            MIX_COLUMNS_COEFFICIENTS
        )
        for i in range(expected.shape[0]):
            for j in range(expected.shape[1]):
                self.assertEqual(expected[i, j], result[i, j])

    def test_encrypt_decrypt(self):
        # Example from Appendix B of the AES Standard
        plaintext = b'\x32\x43\xf6\xa8\x88\x5a\x30\x8d\x31\x31\x98\xa2\xe0\x37\x07\x34'
        ciphertext = b'\x39\x25\x84\x1d\x02\xdc\x09\xfb\xdc\x11\x85\x97\x19\x6a\x0b\x32'
        key = self.KEY.tobytes()
        self.assertEqual(ciphertext, encrypt(plaintext, key))
        self.assertEqual(plaintext, decrypt(ciphertext, key))


if __name__ == '__main__':
    message = input('Please enter a one-line message to encrypt: ')

    key = token_hex(KEY_SIZE)
    print(f'The randomly generated key is {key}.')

    ciphertext = subprocess.run(
        ('python3', 'aesencrypt.py', key, message), capture_output=True
    ).stdout.decode('ascii').rstrip('\n')
    print(f'The ciphertext:', ciphertext)

    plaintext = subprocess.run(
        ('python3', 'aesdecrypt.py', key, ciphertext), capture_output=True
    ).stdout.decode('ascii').rstrip('\n')
    print(f'The decrypted plaintext:', plaintext)
