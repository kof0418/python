from collections import defaultdict


def default_factory():
    return "This is not defined."


# 如果 key 不存在，則會返回 default_factory 結果 (兩種方式)
# d = defaultdict(default_factory)
d = defaultdict(lambda: "Wrong key!!")
d["a"] = 1
d["b"] = 2

print(d["a"], d["b"], d["c"])
