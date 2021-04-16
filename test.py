# import pickle

# asciimoji_saved = str({"<creep>": "ԅ(≖‿≖ԅ)", "crim3s": "( ✜︵✜ )", "cute": "(｡◕‿‿◕｡)"})
# package = "asciimoji"
# with open(package + ".pak", "wb") as FILE:
#     pickle.dump(asciimoji_saved, FILE)
# FILE.close()

with open("asciimoji_package.py", "r") as FILE:
    content = FILE.read()

content = eval(content)
print(type(content))
print(content.keys())
print(content.values())

with open("asciimoji_package_2.py", "w") as FILE:
    FILE.write(sorted(content.keys()))
