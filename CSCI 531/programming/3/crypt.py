from argparse import ArgumentParser
import json
import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

KEY_SIZE = 16

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-e', help='specify the private key file and encrypt the input file')
    parser.add_argument('-d', help='specify the public key file and decrypt the input file')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    args = parser.parse_args()

    if args.e is not None:
        with open(args.e, 'r') as f:
            public_key = json.load(f)

        symmetric_key = secrets.token_bytes(KEY_SIZE)
        nonce = secrets.token_bytes(KEY_SIZE)
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CTR(nonce))
        encryptor = cipher.encryptor()
        with open(args.input_file, 'rb') as f:
            ciphertext = encryptor.update(f.read()) + encryptor.finalize()

        encrypted_symmetric_key = pow(
            int.from_bytes(symmetric_key, 'big'), public_key['e'], public_key['n']
        )
        encrypted_key_length = (encrypted_symmetric_key.bit_length() + 7) // 8
        with open(args.output_file, 'wb') as f:
            f.write(encrypted_key_length.to_bytes(1, 'big'))
            f.write(encrypted_symmetric_key.to_bytes(encrypted_key_length, 'big'))
            f.write(nonce)
            f.write(ciphertext)

    elif args.d is not None:
        with open(args.d, 'r') as f:
            private_key = json.load(f)

        with open(args.input_file, 'rb') as f:
            encrypted_key_length = int.from_bytes(f.read(1), 'big')
            encrypted_symmetric_key = int.from_bytes(f.read(encrypted_key_length), 'big')
            nonce = f.read(KEY_SIZE)

            symmetric_key = pow(
                encrypted_symmetric_key, private_key['d'], private_key['n']
            ).to_bytes(KEY_SIZE, 'big')

            cipher = Cipher(algorithms.AES(symmetric_key), modes.CTR(nonce))
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(f.read()) + decryptor.finalize()

        with open(args.output_file, 'wb') as f:
            f.write(plaintext)
