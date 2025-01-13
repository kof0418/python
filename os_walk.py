import os

# 刪除 1 目錄內所有 .html 類型的檔案
for root, dirs, files in os.walk("1"):
    for f in files:
        filename, filetype = os.path.splitext(f)
        if filetype == '.html':
            os.remove(os.path.join(root, f))
