class Building(object):
    def __init__(self, floors):
        self.__floors = [None] * floors

    def __setitem__(self, floor_number, data):
        self.__floors[floor_number] = data

    def __getitem__(self, floor_number):
        return self.__floors[floor_number]


building1 = Building(4)
building1[0] = 'abc1'
building1[1] = 'def2'
building1[2] = 'ghi3'

for thing in building1:
    print(thing)
