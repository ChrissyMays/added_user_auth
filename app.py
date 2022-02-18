from dataclasses import fields
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ""

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

class QuoteSchema(ma.Schema):
    class Meta:
        fields = ("id", "text", "author")

quote_schema = QuoteSchema()
multiple_quote_schema = QuoteSchema(many=True)
        

if __name__ == "__main__":
    app.run(debug=True, port=8080)

class DateSchema(ma.Schema):
    class Meta:
        fields = ("id", "day", "quote")


date_schema = DateSchema()
multiple_date_schema = DateSchema(many=True)