import pickle
from src.other import InputError, AccessError

# import pickle

# asciimoji_saved = str({"<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"})
# package = "asciimoji"
# with open(package + ".pak", "wb") as FILE:
#     pickle.dump(asciimoji_saved, FILE)
# FILE.close()

# with open("asciimoji_package.py", "r") as FILE:
#     content = FILE.read()

# content = eval(content)
# print(type(content))
# print(content.keys())
# print(content.values())

# with open("asciimoji_package_2.py", "w") as FILE:
#     FILE.write(sorted(content.keys()))


def txt_to_pak(file_name):
    # input checking
    if type(file_name) != str:
        raise InputError(description=f"txt_to_pak : {file_name}.txt not found.")

    try:
        with open(file_name + ".txt", "r") as FILE_1:
            content = eval(FILE_1.read())
    except FileNotFoundError:
        raise InputError(description=f"txt_to_pak : {file_name}.txt not found.")
    with open(file_name + ".pak", "wb") as FILE_2:
        pickle.dump(content, FILE_2)
    FILE_1.close()
    FILE_2.close()


txt_to_pak("asciimoji_lib_1")
