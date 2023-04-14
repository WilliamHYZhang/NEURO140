import sqlite3

connection = sqlite3.connect("database")

c = connection.cursor()

images = c.execute("SELECT * from images").fetchall()

id = 1
for image in images:
    print(image)
    c.execute("UPDATE images SET id=? WHERE id=?", (id, image[0]))
    connection.commit()
    id += 1