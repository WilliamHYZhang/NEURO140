import os
import time

import requests
import sqlite3

from dotenv import load_dotenv

load_dotenv()

AZURE_NEURO140_KEY = os.getenv("AZURE_NEURO140_KEY")
AZURE_ENDPOINT = "https://NEURO140.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=caption&language=en&gender-neutral-caption=False"

connection = sqlite3.connect("database")

c = connection.cursor()

images = c.execute("SELECT * from images").fetchall()

for image in images:
  print("generating caption for image:", image)

  response = requests.post(
    url=AZURE_ENDPOINT,
    headers={
      "Content-Type": "application/json",
      "Ocp-Apim-Subscription-Key": AZURE_NEURO140_KEY,
    },
    json={
      "url": image[1]
    },
  )

  result = response.json()["captionResult"]["text"]

  c.execute(f'''
            UPDATE images set azure_label=? WHERE id=?
            ''',
            (result, image[0]))
  
  connection.commit()

  # rate limit: 20/s
  time.sleep(3)
