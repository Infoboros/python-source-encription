from compiler import Compiler
from config import DIST_PATH, encryptor, MAIN_FILE, SRC_PATH


def compile():
    compiler = Compiler(
        DIST_PATH,
        encryptor,
        MAIN_FILE
    )
    compiler.compile(SRC_PATH)


compile()
