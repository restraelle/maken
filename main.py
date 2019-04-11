# who tf is jason???

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///maken.db"
db = SQLAlchemy(app)

GLOBALS = {}

GLOBALS['frame'] = 0

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(80))
    moniker = db.Column(db.String(40))
    color = db.Column(db.String(6), default="#00ff00")

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(25))
    content = db.Column(db.String(400))

def initDB():
    db.create_all()

def addDummiesToDB():
    testUsers = {
        User(username="raphael", email="me@toxxy.co", password="Password123!", moniker="Not The Ninja Turtle"),
        User(username="chris", email="chris@company.com", password="Password123!", moniker="Christian"),
        User(username="tom", email="tom@company.com", password="Password123!", moniker="Thomas"),
        User(username="yairo", email="yairo@company.com", password="Password123!", moniker="Yairopoop"),
        User(username="tabby", email="tabby@company.com", password="Password123!", moniker="Tabitha")
    }
    db.session.add_all(testUsers)
    db.session.commit()

@app.route('/')
def viewIndex():
    return render_template("index.html")

@app.route('/api/frame', methods=['GET'])
def viewFrame():
    ret = {
        "current_frame": str(GLOBALS['frame'])
    }
    return jsonify(ret)

@app.route('/api/getmessages', methods=['GET'])
def viewAllMessages():
    ret = []
    query = Message.query.all()

    for row in query:
        message = {
            "content": row.content,
            "username": row.username
        }
        ret.append(message)

    return jsonify(ret)

@app.route('/api/post', methods=['GET', 'POST'])
def postMessage():
    # JSON Structure
    # {
    #     "username": "raphael",
    #     "content": "this is a message from the void"
    # }
    try:
        data = request.get_json()
        message = Message(username=data['username'],
                          content=data['content'])
        db.session.add(message)
        db.session.commit()
        GLOBALS['frame'] += 1
        ret = {
            "status": "success"
        }
        return jsonify(ret)

    except:
        ret = {
            "status":"error: failed to receive. sys admin check log"
        }

@app.route('/post', methods=['POST', 'GET'])
def postMessageOld():
    try:
        data = request.get_json()
        print(data)
        if(len(data['Message']) > 0):
            respond = "Success: your message was " + str(data['Message'])
        else:
            respond = "Success: however, your message was empty"
        ret = {
            "message": respond,
            "but also": "why"
        }
        print(data['Message'])
        return jsonify(ret)
    except:
        ret = {
            "message": "internal error: sys admin check log"
        }
        return jsonify(ret)

if(__name__ == "__main__"):
    app.run(debug=True)