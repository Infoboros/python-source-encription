import os
import sys
from types import ModuleType

from config import ENCRYPTED_FILES_EXT, encryptor


# ===============================================================================
class Importer:
    """Служит для поиска и импорта python-модулей, кодированных в base64

    Класс реализует Import Protocol (PEP 302) для возможности импортирования
    модулей, зашифрованных в base64 из указанного пакета.
    """

    # ---------------------------------------------------------------------------
    def __init__(self, root_package_path):

        self.__modules_info = self.__collect_modules_info(root_package_path)

    # ---------------------------------------------------------------------------
    def find_module(self, fullname, path=None):
        """Метод будет вызван при импорте модулей

        Если модуль с именем fullname является base64 и находится в заданной
        папке, данный метод вернёт экземпляр импортёра (finder), либо None, если
        модуль не является base64.
        """
        if fullname in self.__modules_info:
            return self
        return None

    # ---------------------------------------------------------------------------
    def load_module(self, fullname):
        """Метод загружает base64 модуль

        Если модуль с именем fullname является base64, то метод попытается его
        загрузить. Возбуждает исключение ImportError в случае любой ошибки.
        """
        if not fullname in self.__modules_info:
            raise ImportError(fullname)

        mod = sys.modules.setdefault(fullname, ModuleType(fullname))

        mod.__file__ = "<{}>".format(self.__class__.__name__)
        mod.__loader__ = self

        if self.is_package(fullname):
            mod.__path__ = []
            mod.__package__ = fullname
        else:
            mod.__package__ = fullname.rpartition('.')[0]

        src = self.get_source(fullname)

        try:
            exec(src, mod.__dict__)
        except:
            del sys.modules[fullname]
            raise ImportError(fullname)

        return mod

    # ---------------------------------------------------------------------------
    def is_package(self, fullname):
        """Возвращает True если fullname является пакетом
        """
        return self.__modules_info[fullname]['ispackage']

    # ---------------------------------------------------------------------------
    def get_source(self, fullname):
        """Возвращает исходный код модуля fullname в виде строки

        Метод декодирует исходные коды из base64
        """
        filename = self.__modules_info[fullname]['filename']

        try:
            src = encryptor.decrypt_file(filename)
        except IOError:
            src = ''

        return src

    # ---------------------------------------------------------------------------
    @staticmethod
    def __collect_modules_info(root_package_path):
        """Собирает информацию о модулях из указанного пакета
        """
        modules = {}

        p = os.path.abspath(root_package_path)
        dir_name = os.path.dirname(p) + os.sep

        for root, _, files in os.walk(dir_name):
            # Информация о текущем пакете
            filename = os.path.join(root, '__init__.' + ENCRYPTED_FILES_EXT)
            p_fullname = root.rpartition(dir_name)[2].replace(os.sep, '.')

            modules[p_fullname] = {
                'filename': filename,
                'ispackage': True
            }

            # Информация о модулях в текущем пакете
            for f in files:
                if not f.endswith(ENCRYPTED_FILES_EXT):
                    continue

                filename = os.path.join(root, f)
                fullname = '.'.join([p_fullname, os.path.splitext(f)[0]])

                modules[fullname] = {
                    'filename': filename,
                    'ispackage': False
                }

        aliases = {}
        for key, data in modules.items():
            if key.startswith('.'):
                aliases[key[1:]] = data

        return {
            **modules,
            **aliases
        }
