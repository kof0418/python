from collections import Counter

my_list = [1, 2, 2, 3, 3, 3, 1, 1, 3, 2, 2, 3]

# 利用 Counter 統計各種數字總共出現幾次
result = Counter(my_list)

print(result)

leters = "aaaaaaaaaaaaaaaabbbbbbbbbcccccccaaaaaaaaccccccbbbbbb"

# 利用 Counter 英文字母總共出現幾次
c = Counter(leters)

print(c.most_common())
