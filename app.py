from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)
db = SQLAlchemy(app)

class Meme(db.Model):
    __tablename__ = "memes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    url = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(200))

    def __init__(self, title, url, description):
        self.title = title
        self.url = url
        self.description = description

@app.route("/meme/input", methods=["POST"])
def meme_input():
    if request.content_type == "application/json":
        post_data = request.get_json()
        title = post_data.get("title")
        url = post_data.get("url")
        description = post_data.get("description")
        record = Meme(title, url, description)
        db.session.add(record)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify("something went wrong...")

@app.route("/memes", methods=["GET"])
def get_memes():
    all_memes = db.session.query(Meme.id, Meme.title, Meme.url, Meme.description)
    return jsonify(all_memes)

@app.route("/meme/<id>", methods=["GET"])
def get_memes_by_id(id):
    one_meme = db.session.query(Meme.id, Meme.title, Meme.url, Meme.description).filter(Meme.id == id)
    return jsonify(one_meme)

if __name__ == "__main__":
    app.debug = True
    app.run()