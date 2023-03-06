import sqlite3
import random

from cocoapi.PythonAPI.pycocotools.coco import COCO


connection = sqlite3.connect("database")

c = connection.cursor()

# setup dataset
data_directory = 'cocoapi'
data_type = 'val2014'
annotation_file = '{}/annotations/instances_{}.json'.format(data_directory,data_type)

coco=COCO(annotation_file)

# initialize COCO api for caption annotations
annotation_file = '{}/annotations/captions_{}.json'.format(data_directory,data_type)
coco_caps=COCO(annotation_file)

# display COCO categories
categories = coco.loadCats(coco.getCatIds())
print([category['name'] for category in categories])

print(len(categories))

image_ids = set()

# get 5 images and their corresponding labels for each category
for category in categories:
  category_image_ids = coco.getImgIds(catIds=[category["id"]])
  category_image_ids = random.sample(category_image_ids, 5)

  while any(id in image_ids for id in category_image_ids):
    category_image_ids = random.sample(category_image_ids, 5)

  images = coco.loadImgs(category_image_ids)

  for image in images:
    annotation_ids = coco_caps.getAnnIds(image['id'])
    annotation = coco_caps.loadAnns(annotation_ids)[0]

    print(image['id'], image['coco_url'], annotation["caption"])
    
    c.execute(f'''
              INSERT INTO images (id, url, human_label)
              VALUES (?, ?, ?)
              ''',
              (image['id'], image['coco_url'], annotation["caption"]))

connection.commit()



