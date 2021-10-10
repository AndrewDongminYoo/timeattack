import datetime

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os

idx = 0
app = Flask(__name__)
os.popen('mongod')
client = MongoClient("mongodb://localhost:27017/")
db = client.dbStock
col = db.contents


@app.route('/')
def hello_main():
    return render_template('index.html')


@app.route('/posts', methods=['POST'])
def save_post():
    last = list(col.find({}, {"_id": False}).sort("idx", -1))
    global idx
    if not last:
        idx += 1
    else:
        idx = last[0]["idx"]+1
    title = request.form.get('title')
    content = request.form.get('content')
    reg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mod_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    read = 0
    doc = {"idx": idx, 'title': title, 'content': content, 'reg_date': reg_date, "mod_date": mod_date, 'read': read}
    col.insert_one(doc)
    return jsonify({"result": "success", "uploaded": idx})


@app.route('/posts', methods=['GET'])
def get_post():
    contents = list(col.find({}, {"_id": False}).sort("reg_date", -1))
    print(contents)
    return jsonify({"result": "success", "contents": contents})


@app.route('/post/<i>', methods=['GET'])
def read_post(i):
    i = int(i)
    col.update_one({"idx": i}, {"$inc": {"read": +1}})
    content = list(col.find({"idx": i}, {"_id": False}))[0]
    print(content)
    return jsonify({"result": "success", "post": content})


@app.route('/post/<i>', methods=['DELETE'])
def delete_post(i):
    i = int(i)
    col.delete_one({"idx": i})
    return jsonify({"result": "success", "deleted": i})


@app.route('/post/<i>', methods=['PUT'])
def modify_post(i):
    i = int(i)
    title = request.form.get('title')
    content = request.form.get('content')
    mod_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    col.update_one({"idx": i}, {"$set": {"title": title, "content": content, "mod_date": mod_date}})
    return jsonify({"result": "success", "updated": content})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)