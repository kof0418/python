# class Example
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

class Circles:
    """This class creates circle"""
    pi = 3.14159
    all_circles = []

    def __init__(self, radius):
        self.radius = radius
        self.__class__.all_circles.append(self)

    def area(self):
        return self.__class__.pi * (self.radius ** 2)

    # 不建議使用，因為如果 class 名稱更改，這邊名稱沒有同步更改，就會執行錯誤
    @staticmethod
    def total_area():
        total = 0
        for circle in Circle.all_circles:
            total += circle.area()
        return total

    @classmethod
    def total_area2(cls):
        total = 0
        for circle in cls.all_circles:
            total += circle.area()
        return total


c1 = Circles(10)
c2 = Circles(15)
# 如果 class 名稱更改， static
# print(c1.__class__.total_area())
print(c2.__class__.total_area2())
