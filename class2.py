class Robot:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    # define a private method __key()
    def __key(self):
        return (self.name, self.age, self.address)

    # implement __hash__() function
    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, Robot):
            return self.__key() == other.__key()
        return NotImplemented

    def __len__(self):
        return self.age

    def __str__(self):
        return f"{self.name} is now {self.age} years old, living in {self.address}"

    def __repr__(self):
        return f"name: {self.name}, age: {self.age}, address:{self.address}"

    def __add__(self, other):
        if isinstance(other, Robot):
            return self.age + other.age
        return NotImplemented

    # __gt__ 大於 __ge__ 大於等於 __lt__ 小於 __le__ 小於等於
    def __gt__(self, other):
        if isinstance(other, Robot):
            return self.age > other.age
        return NotImplemented


robot1 = Robot("Wilson", 35, "Taiwan")
robot2 = Robot("Wilson", 26, "Taiwan")

# print(robot1)
# print(repr(robot1))
print(robot1 + robot2)
print(robot1 > robot2)
