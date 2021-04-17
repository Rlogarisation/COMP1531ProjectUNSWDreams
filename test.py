from os import curdir
import pickle
import sqlite3
import os
from sqlite3.dbapi2 import Cursor
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


# def txt_to_pak(file_name):
#     # input checking
#     if type(file_name) != str:
#         raise InputError(description=f"txt_to_pak : {file_name}.txt not found.")

#     try:
#         with open(file_name + ".txt", "r") as FILE_1:
#             content = eval(FILE_1.read())
#     except FileNotFoundError:
#         raise InputError(description=f"txt_to_pak : {file_name}.txt not found.")
#     with open(file_name + ".pak", "wb") as FILE_2:
#         pickle.dump(content, FILE_2)
#     FILE_1.close()
#     FILE_2.close()


# txt_to_pak("asciimoji_lib_1")

# os.system("rm -rf test_database.db")
# conn = sqlite3.connect("test_database.db")

# cursor = conn.cursor()
# # 创建表
# # 插入user表
# # id int型　主键自增
# # name varchar型　最大长度２０　不能为空
# cursor.execute('''create table user(id integer primary key autoincrement,name varchar(20) not null)''')

# # 插入记录
# # 插入一条id=1 name='xiaoqiang'的记录
# cursor.execute('''insert into user(id,name) values(1,'xiaoqiang')''')

# # 查找记录
# # 查找user表中id=1的记录
# cursor.execute('''select * from user where id=1''')
# # 获得结果
# values = cursor.fetchall()
# print("values = ", values)

# # 删除记录
# # 删除id=1的记录
# cursor.execute('''delete from user where id=1''')

# # 修改记录
# # 修改id=1记录中的name为xiaoming
# cursor.execute('''update user set name='xiaoming' where id=1''')


from typing import List, Union


def func(a: int, string: str) -> List[int or str]:
    # if type(a) != int:
    #     return "你的a输入类型错了，傻逼"

    list1 = []
    list1.append(a)
    list1.append(string)
    return list1

# 使用or关键字表示多种类型,也可以用Union


def get_next_id(id: int) -> Union[int, None]:
    if not isinstance(id, int):
        return
    if id > 1:
        return id
    return None


print(func(88, "999"))
print(get_next_id(999))

# pycharm会在传入的参数上黄色提示
print(func(88, ["999"]))
print(get_next_id('999'))

print(func([1, 2, 3], "123"))
