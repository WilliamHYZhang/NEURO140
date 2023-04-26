import os
import time

import requests
import sqlite3

from dotenv import load_dotenv

load_dotenv()

connection = sqlite3.connect("database")

c = connection.cursor()

def format_label(s: str):
  ret = s.strip().capitalize()
  if ret[-1] != ".":
    ret += "."
  return ret

images = c.execute("SELECT * from images").fetchall()

count = 0
for image in images:
  id = image[0]
  human_label = format_label(image[2])
  git_label = format_label(image[3])
  azure_label = format_label(image[4])

  c.execute(f'''
            UPDATE images SET human_label=?, git_label=?, azure_label=? WHERE id=?
            ''',
            (human_label, git_label, azure_label, id))
  
  connection.commit()
