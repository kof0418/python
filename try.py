# 算式
# print(10 + 5)
# print(10 + 20)
# print(6 * 3)

# 比大小
# print(min(5, 3))
# print(max(10101, 1002))

# 數學函式
# import math
# print(math.e)
# print(math.pi)

# 計算指定字串數量
# string = "Good day is a good day."
# print(string.count("day"))

# 更改開頭第一個字母
# name = "Jacky Donaldson"
# name = 'P' + name[1:]
# print(name)

# Fstring Example
# myName = "Jacky"
# age = 25
# print(f"Hello, my name is {myName}, I am {age} years old.")

# 增加 list 值，也可以使用不同類型
# friends = ["Wilson", "Mike", "Nelson", "Greg", "Jimmy"]
# friends.append("Aaron")
# print(friends)

# copy list
# x = [1, 2, 3, 4, 5, 6]
# y = x.copy()
# y[0] = 15
# print(x)
# print(y)

# 兩變數互換
# x = 25
# y = 35
# x, y = y, x
# print(x, y)

# list (Array)
# x = [1, 2, [4, 5, 6], 2, 1, [4, 3, [-10, 4]]]
# print(x[5][2][0])

# Dictionary (Object)
# person = {"name": "Jacky", "x": {"age": [18, 30, 42]}}
# print(person["x"]["age"][1])
# x = {'name': 'Jacky', 'age': 26}
# print(x.keys())
# print(x.values())
# print(x.items())

# Tuples
# myTuple = (10, "100", "Hello")
# print(myTuple[0:2])

# Sets
# mySet = set()
# print(mySet)

# List to Sets
# myList = [1, 4, 3, 2, 5, 1, 5]
# mySet = set(myList)
# print(mySet)

# # join Example
# MyList = ['1', '2', '3', '4']
# MyString = '|'.join(MyList)
# print(MyString)

# sorted Example
# x = [4, 3, 1, 2]
# # y = sorted(x)
# y = sorted(x, reverse=True)
# print("the list x is", x, ". Also, the list y is ", y)

# if Example (a 如果裡面有 A，就會顯示)
a = ["A", "B", "C"]
if "A" in a:
    print("A is in ", a)
