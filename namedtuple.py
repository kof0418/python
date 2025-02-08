from collections import namedtuple

worker = namedtuple("worker", ["job", "salary", "workplace"])

jacky = worker("Engineer", 65000, "Taiwan")

print(jacky.job, jacky.workplace)
print(jacky)
