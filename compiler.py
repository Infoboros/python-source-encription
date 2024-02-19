import os
import shutil
from itertools import chain

from encryption import Encryptor


class Compiler:
    STAFF_FILES = [
        'config.py',
        'encryption.py',
        'importer.py'
    ]

    def __init__(self,
                 dist_path: str,
                 encryptor: Encryptor,
                 not_encrypted_files: [str],
                 injection_file: str
                 ):
        self.dist_path = dist_path
        self.encryptor = encryptor
        self.not_encrypted_files = not_encrypted_files
        self.injection_file = injection_file

    def transfer_src_to_dist(self, src_path: str):
        shutil.rmtree(self.dist_path)
        shutil.copytree(src_path, self.dist_path, dirs_exist_ok=True)

    def encrypt(self):
        file_path_for_encrypt = chain(*[
            [
                os.path.join(address, name)
                for name in files
                if name not in self.not_encrypted_files
            ]
            for address, _, files in os.walk(self.dist_path)
        ])
        for file_path in file_path_for_encrypt:
            self.encryptor.encrypt_file(file_path)

    def transfer_staff_files(self):
        for staff_file in self.STAFF_FILES:
            shutil.copy(staff_file, self.dist_path)

    def inject_staff_import(self):
        injection_file_path = os.path.join(self.dist_path, self.injection_file)
        with open(injection_file_path, 'r') as fp:
            data = fp.read()
        with open(injection_file_path, 'w') as fp:
            fp.write('import sys\n')
            fp.write('from importer import Importer\n')
            fp.write('sys.meta_path.append(Importer(__file__))\n')
            fp.write(data)

    def compile(self, src_path: str):
        self.transfer_src_to_dist(src_path)
        self.encrypt()
        self.transfer_staff_files()
        self.inject_staff_import()
