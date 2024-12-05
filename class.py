
## Class Example 1 ##

# class Robot:
#     # Class 備註
#     """Robot class is for creating robots"""

#     # Other method definition
#     ingredient = "metal"

#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def walk(self):
#         print(f"{self.name} is walking...")

#     def sleep(self, hours):
#         print(f"{self.name} is going to sleep for {hours} hours.")

#     def greet(self):
#         # inside method definition
#         # self.__class__ 表示此 class 名稱
#         print(f"Hi, my name is {self.name}, and I am made of {
#               self.__class__.ingredient}.")

# my_robot_1 = Robot("Wilson", 25)
# my_robot_2 = Robot("Grace", 26)

# print(my_robot_1.name)
# print(my_robot_2.age)

# # Class 備註
# print(my_robot_1.__doc__)

# my_robot_2.walk()
# my_robot_1.sleep(15)

# # Other method definition
# print(Robot.ingredient)

# # Outside method definition
# print(my_robot_1.ingredient)

# # Inside method definition
# my_robot_1.greet()

## Class Example 2 ##

# class Circles:
#     """This class creates circle"""
#     pi = 3.14159
#     all_circles = []

#     def __init__(self, radius):
#         self.radius = radius
#         self.__class__.all_circles.append(self)

#     def area(self):
#         return self.__class__.pi * (self.radius ** 2)

#     # 不建議使用，因為如果 class 名稱更改，這邊名稱沒有同步更改，就會執行錯誤
#     @staticmethod
#     def total_area():
#         total = 0
#         for circle in Circle.all_circles:
#             total += circle.area()
#         return total

#     @classmethod
#     def total_area2(cls):
#         total = 0
#         for circle in cls.all_circles:
#             total += circle.area()
#         return total


# c1 = Circles(10)
# c2 = Circles(15)
# # 如果 class 名稱更改， static
# # print(c1.__class__.total_area())
# print(c2.__class__.total_area2())

## Class Example 3 繼承 (可以複寫 function) ##

# class People:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def sleep(self):
#         print(f"{self.name} is sleeping...")

#     def eat(self):
#         print(f"{self.name} is eating food")


# class Stduent(People):
#     def __init__(self, name, age, student_id):
#         # 以下有兩種寫法，另外一種可以用 super()
#         # People.__init__(self, name, age)
#         super().__init__(name, age)
#         self.student_id = student_id

#     def eat(self, food):
#         print(f"{self.name} is now eating {food}")


# student_one = Stduent("Wilson", 25, 100)
# # print(student_one.name, student_one.student_id)
# student_one.eat("beef")

## Class Example 4 (Multiple Inheritance) ##

# class C:
#     def do_stuff(self):
#         print("hello from class C")


# class D:
#     def do_another_stuff(self):
#         print("hello from class D")


# class A(C, D):
#     pass


# a = A()
# a.do_stuff()
# a.do_another_stuff()

# Class Example 5 Private Attributes

# class Robot:
#     def __init__(self, name):
#         self.name = name
#         # private property
#         self.__age = 25

#     def greet(self):
#         print(f"Hi, I am {self.__age} years old.")

#     def get_age(self):
#         return self.__age


# my_robot = Robot("Wilson")
# my_robot.greet()
# print(my_robot.get_age())

# Class Example 6 Private Mothods

# class Robot:
#     def __init__(self, name):
#         self.name = name
#         self.__age = 25

#     # private method
#     def __this_is_private(self):
#         print("Hello from private method")

#     def greet(self):
#         print("Hi, I am a robot")
#         self.__this_is_private()


# my_robot = Robot("Wilson")
# my_robot.greet()

# Class Example 7 使用 private Attributes 才不會輕易被修改，需要使用 class 內 function 才能修改與取得

# class Robot:
#     def __init__(self, name):
#         self.name = name
#         self.__age = 25

#     def age_setter(self, new_age):
#         if new_age > 0 and new_age < 100:
#             self.__age = new_age
#         else:
#             print("New age setting is invalid")

#     def age_getter(self):
#         print(self.__age)


# my_robot = Robot("Wilson")
# my_robot.age_setter(50)
# my_robot.age_getter()

# Class Example 8 @property decorator

# class Employee:
#     def __init__(self):
#         self.income = 0

#     def earn_money(self, money):
#         self.income += money

#     @property
#     def tax_amount(self):
#         return self.income * 0.05

#     @tax_amount.setter
#     def tax_amount(self, tax_number):
#         self.income += tax_number * 20


# wilson = Employee()
# # wilson.earn_money(300)
# # print(wilson.tax_amount)


# wilson.tax_amount = 200
# print(wilson.income)
