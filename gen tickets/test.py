import sqlite3

connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()

# cur.execute("""
# CREATE TABLE TedXDypit(
#     ID INTEGER PRIMARY KEY AUTOINCREMENT,
#     Name varchar(255),
#     Number varchar(255), 
#     Email varchar(255) UNIQUE, 
#     Type varchar(255),
#     Payment_Methord varchar(255),
#     Screenshot varchar(255),
#     Approved varchar(255),
#     Attended varchar(255)
# )
# """)

# query = f"SELECT Name, Number, Email, Screenshot FROM TedXDypit WHERE Approved='N'"
# cur.execute(query)
# data = cur.fetchall()
# t = ""
# for i in data:
#     t += i[0]
#     t += ", "
#     t += i[1]
#     t += ", "
#     t += i[2]
#     t += ", "
#     t += "https://drive.google.com/open?id=" + i[3]
#     t += "\n"

# with open("failures.txt", 'w') as f:
#     f.write(t)

# query = "UPDATE TedXDypit SET Approved='Y' WHERE Approved IS NULL"

# query = "SELECT * FROM TedXDypit"
# cur.execute(query)
# data = cur.fetchall()
# t = '\n'.join([f'{", ".join(str(e) for e in i)}' for i in data])
# with open('export.csv', 'w') as f:
#     f.write(t)

# query = "DROP TABLE emails"
# cur.execute(query)

# query = "CREATE TABLE emails(ID INTEGER PRIMARY KEY AUTOINCREMENT, Email varchar(255))"
# cur.execute(query)
connection.commit()