
# file.read() returns a string.
# file = open("note.txt")
# print(file.read())
# file.close()

# 讀取過一次，還要從頭開始讀取，可以用 file.seek
# file = open("note.txt")
# print(file.read())
# print('-----------------------')
# file.seek(0)
# print(file.read())
# file.close()

# file.readlines returns a list.
# file = open("note.txt")
# # print(file.readlines())
# for line in file.readlines():
#     print(line)
# file.close()

# file.readline
# file = open("note.txt")
# while True:
#     line = file.readline()
#     if line == "":
#         break
#     else:
#         print(line)
# file.close()

# with 語法，不用擔心需要 close file
# with open("note.txt") as my_file:
#     all_content = my_file.read()
#     print(all_content)

# mode="a" 增加資料，mode="w" 複寫
# with open("note.txt", mode="w") as my_file:
#     my_file.write("Learning python is os fun.\nLearning JavaScript is so fun.")

# encoding 指定編碼
# with open("note.txt", mode="w", encoding="utf-8") as my_file:
#     my_file.write("Learning python is os fun.\nLearning JavaScript is so fun.")

# os.remove filename
# import os
# os.remove("index.html")

# # os.rmdir foldername
# import os
# os.rmdir("new_folder")

# user_input = input("How old are you?")
# user_address = input("Where do you live?")
# print("--------------------------")
# print(user_input)
# print(type(user_input))

# 終極密碼
# import random
# secret = random.randint(1, 100)
# min_value = 1
# max_value = 100
# # print(secret)
# while True:
#     guess = input(f"Make your guess (between {min_value} and {max_value}): ")
#     if int(guess) < min_value or int(guess) > max_value:
#         print("Your guess is not within the range!!")
#         continue
#     if int(guess) == secret:
#         print(f"The secret is {secret}")
#         break
#     elif int(guess) < secret:
#         min_value = int(guess)
#     elif int(guess) > secret:
#         max_value = int(guess)
