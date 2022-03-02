from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://wkcxtlsrywnsoe:95cb0e21d62808d52800be5caf494689e82aa9051cfba1c63f01e693f4e02270@ec2-54-157-160-218.compute-1.amazonaws.com:5432/d1kid9j526m8ej"

db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)

class Quote(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    author = db.Column(db.String)

    def __init__(self, text, author):
        self.text = text
        self.author = author 

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    quote = db.Column(db.Integer, nullable=False)

    def __init__(self,day,quote):
        self.day = day
        self.quote = quote

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __init__(self,username, password):
        self.username = username
        self.password = password
class QuoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "author")

quote_schema = QuoteSchema()
multiple_quote_schema = QuoteSchema(many=True)
        
class DateSchema(ma.Schema):
    class Meta:
        fields = ("id", "day", "quote")


date_schema = DateSchema()

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password") #TODO Remove sensitive fields

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route("/quote/add", methods=["POST"])
def add_quote():
    if request.content_type != "application/json":
        return jsonify ("ERROR: Data must be sent as JSON.")


    post_data = request.get_json()
    text = post_data.get("text")
    author = post_data.get("author")

    record = Quote(text, author)
    db.session.add(record)
    db.session.commit()

    return jsonify(quote_schema.dump(record))

@app.route("/quote/get/<id>", methods=["GET"])
def get_quote_by_id(id):
     records = db.session.query(Quote).filter(Quote.id == id).first()
     print(record)
     return jsonify(quote_schema.dump(record))


@app.route("/date/add", methods=["POST"])
def create_initial_date():
    record_check = db.session.query(Date).first()
    if record_check is not None:
        return jsonify("Error: Date has already been initialized")

    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")


    post_data = request.get_json()
    day = post_data.get("day")
    quote = post_data.get("quote")

    record = Date(day, quote)
    db.session.add(record)
    db.session.commit()

    return jsonify(date_schema.dump(record))

@app.route("/date/get", methods=["GET"])
def get_date():
    record = db.session.query(Date).first()
    return jsonify(date_schema.dump(record))

@app.route("/date/update", methods=["PUT"])
def update_date(): 
    record = db.session.query(Date).first()
    if record is None: 
        return jsonify("Error date has not been initialized")

    if request.content_type != "application/json":
        return jsonify("Error Data must be sent as JSON")

    put_data = request.get_json()
    day = put_data.get("day")

    all_quotes = db.session.query(Quote).all()
    current_quote = db.session.query(Quote).filter(Quote.id == record.quote).first()
    current_quote_index = all_quotes.index(current_quote)
    if current_quote_index + 1 < len(all_quotes):
        next_quote = all_quotes[current_quote_index + 1]
    else:
        next_quote = all_quotes[0]
    

    record.day = day 
    record.quote = next_quote.id
    db.session.commit()

    return jsonify(date_schema.dump(record))


@app.route("/user/add", methods=["POST"])
def add_user():
    if request.content_type != "application/json":
       return jsonify ("ERROR: Data must be sent as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    record = User(username, password)
    db.session.add(record)
    db.session.commit()

    return jsonify(user_schema.dump(record))

    record_check = db.session.query(User).filter(User.username == username).first
    if record_check is not None:
        return jsonify("Error: Username already exists.")

@app.route("/user/login", methods=["POST"])
def login():
    if request.content_type != "application/json":
       return jsonify ("ERROR: Data must be sent as JSON.")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    record = db.session.query(User).filter(User.username == username).first()
    if record is None:
        return jsonify("User login not verified")

    if record.password != password:
        return jsonify("User login not verified")

    return jsonify("User verified!")

if __name__ == "__main__":
    app.run(debug=True, port=8080)

