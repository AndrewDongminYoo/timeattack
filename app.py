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
    if not col.find({}):
        idx = 0
        print(request.form)
    idx = len(col.find({}))
    content = request.form.get('content')
    reg_date = datetime.datetime.now()
    doc = {"idx": idx, 'content': content, 'reg_date': reg_date}
    col.insert_one(doc)
    return jsonify({"result": "success", "uploaded": idx})


@app.route('/post', methods=['DELETE'])
def get_post():
    idx = request.args.get('idx')
    print(idx)
    col.delete_one({"idx": idx})
    return jsonify({"result": "success", "deleted": idx})


@app.route('/post', methods=['GET'])
def delete_post():
    contents = col.find({}, {"_id": False}).sort({"reg_date": -1})
    print(contents)
    return jsonify({"result": "success", "contents": contents})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)