import base64
import os
from abc import ABC, abstractmethod


class Encryptor(ABC):
    def __init__(self, encrypted_files_ext: str):
        self.encrypted_files_ext = encrypted_files_ext

    @abstractmethod
    def encrypt_file(self, file_path: str):
        raise NotImplemented()

    @abstractmethod
    def decrypt_file(self, file_path: str) -> str:
        raise NotImplemented()


class Base64Encryptor(Encryptor):
    def decrypt_file(self, file_path: str):
        with open(file_path) as fp:
            return base64.decodebytes(fp.read().encode()).decode()

    def encrypt_file(self, file_path):
        with open(file_path) as fp:
            data = fp.read()

        with open(file_path, 'w') as fp:
            fp.write(
                base64
                .encodebytes(data.encode())
                .decode()
            )

        dir_name = os.path.dirname(file_path)
        file = os.path.basename(file_path)

        file_name, _ = os.path.splitext(file)

        os.rename(
            file_path,
            os.path.join(
                dir_name,
                f'{file_name}.{self.encrypted_files_ext}'
            )
        )
