import os

import sqlite3

from GenerativeImage2Text.generativeimage2text import inference

connection = sqlite3.connect("database")

c = connection.cursor()

images = c.execute("SELECT * from images").fetchall()

os.chdir("GenerativeImage2Text")

for image in images:
  print("generating caption for image:", image)

  # id, url, human_label, git_label, azure_label
  result = inference.test_git_inference_single_image(
    image_path=image[1],
    model_name="GIT_BASE",
    prefix="",
    )

  c.execute(f'''
            UPDATE images set git_label=? WHERE id=?
            ''',
            (result, image[0]))
  
  connection.commit()
