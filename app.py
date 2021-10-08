import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock
col = db.contents


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def save_post():
    idx = col.count({})+1
    title = request.form.get('title')
    content = request.form.get('content')
    reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mod_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    read = 0
    doc = {"idx": idx, 'title': title, 'content': content, 'reg_date': reg_date, "mod_date": mod_date, 'read': read}
    col.insert(doc)
    return jsonify({"result": "success", "uploaded": idx})


@app.route('/post', methods=['DELETE'])
def get_post():
    idx = request.args.get('idx')
    print(idx)
    col.delete_one({"idx": idx})
    return jsonify({"result": "success", "deleted": idx})


@app.route('/post', methods=['GET'])
def delete_post():
    contents = list(col.find({}, {"_id": False}).sort("reg_date", -1))
    print(contents)
    return jsonify({"result": "success", "contents": contents})


@app.route('/detail/<idx>', methods=['GET'])
def read_post(idx):
    col.update_one({"idx": idx}, {"$inc": {"read": +1}})
    content = list(col.find({"idx": idx}, {"_id": False}))
    print(content)
    return jsonify({"result": "success", "updated": content})


@app.route('/update/<idx>', methods=['PUT'])
def modify_post(idx):
    title = request.form.get('title')
    content = request.form.get('content')
    mod_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    col.update_one({"idx": idx}, {"$set": {"title": title, "content": content, "mod_date": mod_date}})
    return jsonify({"result": "success", "updated": content})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)