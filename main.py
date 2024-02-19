from compiler import Compiler
from config import DIST_PATH, encryptor, NOT_ENCRYPTED_FILES, SRC_PATH, INJECTION_FILE


def compile():
    compiler = Compiler(
        DIST_PATH,
        encryptor,
        NOT_ENCRYPTED_FILES,
        INJECTION_FILE
    )
    compiler.compile(SRC_PATH)


compile()
