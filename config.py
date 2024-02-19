import os
from pathlib import Path

from encryption import Base64Encryptor

BASE_PATH = Path(__file__).resolve().parent
SRC_PATH = os.path.join(BASE_PATH, 'src')
DIST_DIR = 'dist'
DIST_PATH = os.path.join(BASE_PATH, 'dist')

NOT_ENCRYPTED_FILES = ['main.py']
INJECTION_FILE = 'main.py'

ENCRYPTED_FILES_EXT = 'enc'

encryptor = Base64Encryptor(ENCRYPTED_FILES_EXT)
