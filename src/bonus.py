# Here is bonus functions
from src.data_file import data
from src.other import InputError, AccessError
from src.auth import get_user_by_token
import pickle


def asciimoji_import_package(token, package, pkg_type):
    user = get_user_by_token(token)
    if pkg_type == "pak":
        try:
            with open(package + ".pak", "rb") as FILE:
                asciimoji_load = pickle.load(FILE)
        except FileNotFoundError:
            raise InputError(description=f"asciimoji_import_package : {package}.pak not found.")
    elif pkg_type == "txt":
        try:
            with open(package + ".txt", "r") as FILE:
                asciimoji_load = FILE.read()
        except FileNotFoundError:
            raise InputError(description=f"asciimoji_import_package : {package}.txt not found.")

    user.asciimoji.update(eval(asciimoji_load))
    FILE.close()


def asciimoji_export_package(token, package, pkg_type):
    user = get_user_by_token(token)

    asciimoji_saved = str(user.asciimoji)

    if pkg_type == "pak":
        with open(package + ".pak", "wb") as FILE:
            pickle.dump(asciimoji_saved, FILE)
    elif pkg_type == "txt":
        with open(package + ".txt", "w") as FILE:
            FILE.write(asciimoji_saved)

    FILE.close()


def txt_to_pak(file_name):

    try:
        with open(file_name + ".txt", "r") as FILE_1:
            content = eval(FILE_1.read())
    except FileNotFoundError:
        raise InputError(description=f"txt_to_pak : {file_name}.txt not found.")
    with open(file_name + ".pak", "wb") as FILE_2:
        pickle.dump(content, FILE_2)
    FILE_1.close()
    FILE_2.close()


def pak_to_txt(file_name):
    try:
        with open(file_name + ".pak", "rb") as FILE_1:
            content = eval(pickle.load(FILE_1))
    except FileNotFoundError:
        raise InputError(description=f"pak_to_txt : {file_name}.txt not found.")
    with open(file_name + ".txt", "w") as FILE_2:
        FILE_2.write(content)
    FILE_1.close()
    FILE_2.close()
