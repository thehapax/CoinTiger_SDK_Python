from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import logging, os
import binascii
import base64

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

def gen_key(passwd):
    try:
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(passwd)
        return base64.urlsafe_b64encode(digest.finalize())
    except Exception as e:
        log.info("Gen_key Exception: %s ", e)


def encrypt_file(input_passwd, my_config):
    try:
        my_password = bytes(input_passwd, encoding='utf-8')
        log.info(my_password)

        if (len(my_password)>1):
            key = gen_key(my_password)
            log.info("Key: %s ", binascii.hexlify(bytearray(key)))

            cipher_suite = Fernet(key)
            cipher_text = cipher_suite.encrypt(my_config)
            return cipher_text
    except Exception as e:
        log.info("Encrypt_file Exception: %s",  e)


def decrypt_file(input_passwd, cipher_text):
    try:
        my_password = bytes(input_passwd, encoding='utf-8')
        key = gen_key(my_password)
        cipher_suite = Fernet(key)
        plain_text = cipher_suite.decrypt(cipher_text).decode('utf-8')
        return plain_text
    except Exception as e:
        log.info("Decrypt_file Exception: %s", e)


