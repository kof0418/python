
# help
# myList = [1, 2, 3, 4]
# myList.insert(2, 10)
# help(myList.insert)

# def functionName(input1, input2, ...):
#    function code here

# function example 1
# def addition(x, y):
#     print(x + y)
#
# a = 30
# b = 25
# addition(a, b)

# Global variables & Local variables
# a = 5  # global variable
# def f1():
#     x = 2  # local variable
#     y = 3
#     print(x, y, a)
#
# f1()

# 如果 function 要更改 global variable，需要在 function 內加上 global
# a = 10
#
# def change(num):
#     global a
#     a = 25
#
# change(a)
# print(a)

# function 新增 help 備註說明
# def myAddition(a, b):
#     """This function does addtion"""
#     print(a + b)
# help(myAddition)

# function return keyword
# def myAddition(a, b):
#     return (a + b)
# print(myAddition(10, 18)+myAddition(26, 19)+myAddition(15, 17))

# function return keyword 2
# def myAddition(a, b):
#     for i in range(a):
#         for j in range(b):
#             if i == 3 and j == 4:
#                 return
#             print(i, j)
# myAddition(10, 15)

# keyword arguments1
# def exponent(a, b):
#     return a ** b
# print(exponent(b=2, a=10))

# Default Arguments2 n2=0
# def sum(n1, n2=0):
#     return n1 + n2
# print(sum(12))

# Arbitrary Number of Arguments (*args)
# def sum(*args):
#     result = 0
#     for number in range(0, len(args)):
#         result += args[number]
#         print(f"Now, the result is {result}")
#     return result
# print(sum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))

# Default Arguments (**kwargs)
# def myfunc(**kwargs):
#     print("{} is now {} years old.".format(kwargs["name"], kwargs["age"]))
# myfunc(name="Wilson", age=26, address="Hawaii")

# Default Arguments (*args) + (**kwargs)
# def myfunc(*args, **kwargs):
#     print("I would like to eat {} {}".format(args[1], kwargs["food"]))
# myfunc(14, 17, 23, "Hello", name="Wilson", food="eggs")

# Higher-Order Function
# def higherOrder(fn):
#     fn()
# def smallfunc():
#     print("Hello from smaill function.")
# higherOrder(smallfunc)

# Higher-Order Function map()
# def square(num):
#     return num ** 2
# myList = [-10, 3, 9, 8, 10]
# for item in map(square, myList):
#     print(item)

# Higher-Order Function filter() 檢查myList哪些是偶數
# def even(num):
#     return num % 2 == 0
# myList = [444532, 3211543, -998432, 66154]
# for item in filter(even, myList):
#     print(item)

# Lambda input1, input2, ...: operation 1
# myTuple = (lambda x, y: (x + y, x - y))(15, 30)
# print(myTuple[0])
# print(myTuple[1])

# Lambda input1, input2, ...: operation 2
# for item in map(lambda x: x**2, [15, 10, 5, 0]):
#     print(item)

# Lambda input1, input2, ...: operation 3
# for item in filter(lambda x: x % 2 == 0, [15, 10, 5, 0]):
#     print(item)

# Scope (這時候name會顯示Grace，不會是Wilson，因為是在不同層)
# name = "Wilson"
# def greet():
#     name = "Grace"
#     def hello():
#         print("Hello, my name is " + name)
#     hello()
# greet()
