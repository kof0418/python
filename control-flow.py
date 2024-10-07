# If example
# if True:
#     print("This is so True")
# else:
#     print("This is so False")

# if example2
# age = 15
# if age < 8:
#     print("Movie is free for you!!")
# elif 8 <= age < 65:
#     print("You need to pay $300!")
# else:
#     print("You only need to pay $150")

# For example List 1
# myList = [1, 3, 5, 7, 9]
# for num in myList:
#     print(num)

# For example Tuple 2
# for a, b in [(1, 2), (3, 5), (5, 7)]:
#     print(a + b)

# For example Dictionary 3
# myDictionary = {"name": "Wilson", "age": 25}
# for item in myDictionary.items():
#     print(item)

# For example Set 4
# for i in {1, 3, 5, 7, 9}:
#     print(i)

# While Loop example 1
# x = 0
# while x < 5:
#     print(x)
#     x += 1

# While Nested Loop example 2
# for i in "1234":
#     for j in "abcdefg":
#         print(i, j)

# Pass
# for i in "How are you?":
#     pass
# print("hello")

# Break
# for i in "123456789":
#     if i == "5":
#         break
#     else:
#         print(i)

# Continue
# for i in "ABCDE":
#     if i == "B":
#         continue
#     print(i)

# Range Function
# for i in range(0, 100, 4):
#     print(i)

# Enumerate Function
# for item in enumerate("How are you today?"):
#     print(item)

# Zip Function (只會顯示最短的長度)
# x = [1, 2, 3]
# y = ['A', 'B', 'C']
# z = ['a', 'b', 'c', 'c']
# for tuple in zip(x, y, z):
#     print(tuple)

# Structural Pattern Matching example ( > 3.10 Support )
# lang = input("你希望學什麼程式語言?")
# match lang:
#     case "JavaScript" | "JavaScript2":
#         print("你會成為網頁前端開發人員")
#     case "PHP":
#         print("你會成為網頁後端開發人員")
#     case "Python":
#         print("你會成為資料科學家")
#     case "Kotlin":
#         print("你會成為Android應用程式開發人員")
#     case "Swift":
#         print("你會成為IOS應用程式開發人員")
#     case _:
#         print("你會成為其他開發人員")

# Structural Pattern Matching example 2 ( > 3.10 Support )
# command = input("Where do you wanna go?")
# match command.split(" "):
#     case ["Go", "home"]:
#         print("You wanna home home.")
#     case _:
#         print("The system cannot determine where you wanna go.")
