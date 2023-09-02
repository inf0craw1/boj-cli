import json

from cryptography.fernet import Fernet

from boj.core.data import Credential
from boj.core.error import AuthenticationError
from boj.core.property import key_file_path, credential_file_path
from boj.core.util import read_file


def create_key():
    k = Fernet.generate_key()
    return k


def encrypt(k, p):
    f = Fernet(k)
    c = f.encrypt(bytes(p, "utf-8"))
    return c


def decrypt(k, c):
    f = Fernet(k)
    p = f.decrypt(c).decode("utf-8")
    return p


def read_credential() -> Credential:
    try:
        key = read_file(key_file_path(), "rb")
        credential = read_file(credential_file_path(), "rb")
        decrypted = json.loads(decrypt(key, credential))

        return Credential(username=decrypted["username"], token=decrypted["token"])
    except Exception as e:
        print(e)
        raise AuthenticationError()
