import sqlite3

conn = sqlite3.connect("datafile.db")
cursor = conn.cursor()

# print(result.fetchall())
# print(result.fetchmany(2))

# result = cursor.execute(
#     "select * from people where name=:username", {"username": "Grace"})
# print(result.fetchall())

# cursor.execute("""update people set count = :usercount where name = :username""", {
#                "username": 'Bob', "usercount": 39})

# cursor.execute("""Delete from people where name = 'Grace'""")

# result = cursor.execute("select * from people")
# print(result.fetchall())

conn.commit()
conn.close()
