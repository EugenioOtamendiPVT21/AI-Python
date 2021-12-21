from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BookModel(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String(),unique = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Integer())
    author = db.Column(db.String(80))

    def __init__(self, book_id, name, price, author):
        self.book_id = book_id
        self.name = name
        self.price = price
        self.author = author

    def json(self):
        return {"book_id":self.book_id, "name":self.name, "price":self.price, "author":self.author}

    def __repr__(self):
        a= '{}, {}, {}, {}'.format(self.book_id , self.name , self.price , self.author)
        return a


