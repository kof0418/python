# https://www.w3schools.com/python/python_datetime.asp

import datetime

# 類似 Linux date 指令
# x = datetime.datetime.now()
# print(x)
# print(x.year)
# print(x.month)
# print(x.day)

# 計算目前與 2020/1/1 隔多久
now = datetime.datetime.now()
oneday = datetime.datetime(2020, 1, 1)
diff = now - oneday

print(diff)
print(diff.days)
print(diff.total_seconds())
