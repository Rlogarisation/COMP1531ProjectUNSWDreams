# Here is bonus functions
from src.data_file import data
from src.other import InputError, AccessError
from src.auth import get_user_by_token


def asciimoji_import(token):
    user = get_user_by_token(token)
    user_name = user.name_first + user.name_last
    try:
        import_file = open(f"{user_name}_asciimoji.txt", "r")
        import_asciimoji = eval(import_file.read())
    except FileNotFoundError:
        warning = f"asciimoji : could not find your personal asciimoji file {user_name}_asciimoji.txt."
        raise InputError(description=warning)
    user.asciimoji.update(import_asciimoji)
    import_file.close()


def asciimoji_export(token):
    user = get_user_by_token(token)
    user_name = user.name_first + user.name_last

    export_file = open(f"{user_name}_asciimoji.txt", "w")
    export_file.write(str(user.asciimoji))
    export_file.close()
