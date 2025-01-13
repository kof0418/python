import os
import sys

# 取得當前上一層目錄 (Linux適用)
# print(os.pardir)

# 取得指定目錄內檔案與資料夾列表 (Linux & Windows 都適用)
print(os.listdir(os.curdir))

# 路徑名稱正確寫法 (自動識別系統)
# print(os.path.join("utils", "hello.html"))

# 路徑 與 檔案 分開
# filepath = "whatever\\some\\directory\\path.jpg"
# # print(os.path.split(filepath))
# print(os.path.basename(filepath))
# print(os.path.dirname(filepath))

# 取得檔案副檔名
# filepath = "whatever\\some\\directory\\path.jpg"
# print(os.path.splitext(filepath))

# 取得絕對路徑
# filepath = "whatever\\some\\directory\\path.jpg"
# print(os.path.abspath(filepath))

# 取得作業系統相關資訊
# print(os.name)
# print(sys.platform)

# 確認是目錄還是檔案，或者是否存在
# print(os.path.isfile("C:\\Users\\jacky\\OneDrive\\Github\\python"))
# print(os.path.isdir("C:\\Users\\jacky\\OneDrive\\Github\\python"))
# print(os.path.exists("C:\\Users\\jacky\\OneDrive\\Github\\python"))

# 更改名稱、刪除檔案、建立目錄、刪除目錄
# os.rename("C:\\Users\\jacky\\OneDrive\\Github\\python\\kof0419",
#           "C:\\Users\\jacky\\OneDrive\\Github\\python\\kof0418")
# os.remove("C:\\Users\\jacky\\OneDrive\\Github\\python\\kof0418")
# os.mkdir("C:\\Users\\jacky\\OneDrive\\Github\\python\\kof0418")
# os.rmdir("C:\\Users\\jacky\\OneDrive\\Github\\python\\kof0418")
