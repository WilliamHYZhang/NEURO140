import random

import flask
import sqlite3


connection = sqlite3.connect("database", check_same_thread=False)

c = connection.cursor()

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return flask.render_template("index.html")

@app.route("/test/<id>")
def test(id):
    # get image
    images = c.execute(f'''
                      SELECT * from images WHERE id=?
                      ''',
                      (id,)).fetchall()

    connection.commit()
    
    if len(images) == 0:
        return {
            "error": "Invalid image ID."
        }

    image = images[0]

    url = image[1]
    human_label = image[2]
    git_label = image[3]
    azure_label = image[4]


    # choose random ai label
    ai_label = random.choice([git_label, azure_label])

    # shuffle human/ai label order
    labels = [human_label, ai_label]
    random.shuffle(labels)

    label1, label2 = labels

    return flask.render_template("test.html", id=id, url=url, label1=label1, label2=label2)

@app.route("/statistics", methods=["GET"])
def get_statistics():
    # calculate statistics
    git_correct = c.execute("SELECT COUNT (*) FROM statistics WHERE label_type='git' AND correct=1").fetchone()[0]
    git_total = c.execute("SELECT COUNT (*) FROM statistics WHERE label_type='git'").fetchone()[0]
    git_percentage = f"{git_correct/git_total:.2%}"

    azure_correct = c.execute("SELECT COUNT (*) FROM statistics WHERE label_type='azure' AND correct=1").fetchone()[0]
    azure_total = c.execute("SELECT COUNT (*) FROM statistics WHERE label_type='azure'").fetchone()[0]
    azure_percentage = f"{azure_correct/azure_total:.2%}"

    connection.commit()

    return flask.render_template("statistics.html", stats=[["GIT", git_correct, git_total, git_percentage], ["AZURE", azure_correct, azure_total, azure_percentage]])
    

@app.route("/statistics", methods=["POST"])
def post_statistics():
    # get form inputs
    id = int(flask.request.form.get("id"))
    label1 = flask.request.form.get("label1")
    label2 = flask.request.form.get("label2")
    human_label = flask.request.form.get("human_label")
    
    # get image
    images = c.execute(f'''
                      SELECT * from images WHERE id=?
                      ''',
                      (id,)).fetchall()

    connection.commit()
    
    if len(images) == 0:
        return {
            "error": "Invalid image ID."
        }

    image = images[0]
    
    # get statistics
    url = image[1]
    true_human_label = image[2]
    git_label = image[3]

    label_type = "git" if git_label in [label1, label2] else "azure"
    correct = true_human_label == human_label
    
    # populate db
    c.execute(f'''
            INSERT INTO statistics (id, url, label_type, correct)
            VALUES (?, ?, ?, ?)
            ''',
            (id, url, label_type, correct))

    connection.commit()

    if id == 400:
        return {
            "success": True
        }

    return flask.redirect("/test/" + str(id+1))