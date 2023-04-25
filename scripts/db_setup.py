import sqlite3

connection = sqlite3.connect("database")

c = connection.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS images
          ([id] INTEGER PRIMARY KEY, [url] TEXT, [human_label] TEXT, [git_label] TEXT, [azure_label] TEXT)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS statistics
          ([id] INTEGER, [url] TEXT, [label_type] TEXT, [correct] INTEGER)
          ''')

c.execute('''
          CREATE INDEX id_index ON statistics(id)
          ''')

c.execute('''
          CREATE INDEX label_type_index ON statistics(label_type)
          ''')

connection.commit()