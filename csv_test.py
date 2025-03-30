import csv

# 開啟 CSV
# with open("file.csv", newline="", encoding="cp950") as f:
#     csv_data = csv.reader(f)
#     for row in csv_data:
#         print(row)

# 寫入 CSV
with open("new.csv", mode="w", newline="", encoding="cp950") as f:
    csv_writer = csv.writer(f, delimiter=",")
    csv_writer.writerow(['a', 'b', 'c'])
