from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource, reqparse, abort
from models import db, BookModel

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db.init_app(app)

#   will be executed once, before ant user arrives to the site,
#   before the first request arrives
@app.before_first_request
def create_table():
    db.create_all()
#   now coding the create view
#   The Create view should be able to do the following:
#   When the Client goes to this page (GET method), it should display a Form to get the Client’s Data.
#   On Submission (POST method), it should save the Client’s data in the BookModel Database.
@app.route('/booksWeb/create' , methods = ['GET','POST']) #map the specific URL with the associated function
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        book_id = request.form['book_id']
        name = request.form['name']
        price = request.form['price']
        author = request.form['author']
        books = BookModel(book_id=book_id, name=name, price=price, author = author)
        db.session.add(books)
        db.session.commit()
        #return redirect('/books')
        books = BookModel.query.all()
        return render_template('datalist.html',books = books)

#now coding the retrieve views
#Here we will have 2 views:
# First to display the list of Books.
@app.route('/')
@app.route('/booksWeb')
def RetrieveDataList():
    books = BookModel.query.all()
    return render_template('datalist.html',books = books)


#SecondtTo display the information of a single Book.
"""--- BookModel.query.filter_by(book_id = book_id).first() 
will return the first Book with Book Id = book_id in the DB 
or return "Book doest not exist" if the Book with that nme does not exist. ---"""
@app.route('/booksWeb/<book_id>')
def RetrieveSingleBook(book_id):
    book = BookModel.query.filter_by(book_id = book_id).first()
    if book:
        return render_template('data.html', book = book)
    return "Book doest not exist"

# Coding the update view
#The Update View will update the Book details in the DB with the new one submitted by the user
#Here we first delete the old information present in the DB and then add the new information
@app.route('/booksWeb/<book_id>/update',methods = ['GET','POST'])
def update(book_id):
    book = BookModel.query.filter_by(book_id=book_id).first()
    if request.method == 'POST':
        if book:
            db.session.delete(book)
            db.session.commit()
            book_id = request.form['book_id']
            name = request.form['name']
            price = request.form['price']
            author = request.form['author']
            book = BookModel(book_id= book_id, name=name, price=price, author = author)

            db.session.add(book)
            db.session.commit()
            #return redirect('/booksWeb/{name}')
            return render_template('data.html',book = book)
        return "Book does not exist"

    return render_template('update.html', book = book)

#Coding the delete view
#The Delete View will just delete the Book Information from the DB File.
@app.route('/booksWeb/<book_id>/delete', methods=['GET','POST'])
def delete(book_id):
    book = BookModel.query.filter_by(book_id=book_id).first()
    if request.method == 'POST':
        if book:
            db.session.delete(book)
            db.session.commit()
            #return redirect('/booksWeb')
            return render_template('data.html',book = book)
        abort(404)

    return render_template('delete.html')



#Classes to work with json resourses and postman
class BooksView(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('book_id',
                        type=str,
                        required=True,
                        help = "Can't leave blank"
                        )
    parser.add_argument('name',
        type=str,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
    )

    def get(self):
        books = BookModel.query.all()
        return {'Books':list(x.json() for x in books)}

    def post(self):
        data = request.get_json()
        #data = BooksView.parser.parse_args()

        new_book = BookModel(data['book_id'],data['name'],data['price'],data['author'])
        db.session.add(new_book)
        db.session.commit()
        return new_book.json(),201


class BookView(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('book_id',
                        type=str,
                        required=True,
                        help = "Can't leave blank"
                        )
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help = "Can't leave blank"
                        )
    parser.add_argument('price',
        type=float,
        required=True,
        help = "Can't leave blank"
        )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
        )

    def get(self,book_id):
        book = BookModel.query.filter_by(book_id=book_id).first()
        if book:
            return book.json()
        return {'message':'book not found'},404

    def put(self,book_id):
        data = request.get_json()
        #data = BookView.parser.parse_args()

        book = BookModel.query.filter_by(book_id=book_id).first()

        if book:
            book.name = data["name"]
            book.price = data["price"]
            book.author = data["author"]
        else:
            book = BookModel(book_id = book_id,**data)

        db.session.add(book)
        db.session.commit()

        return book.json()

    def delete(self,book_id):
        book = BookModel.query.filter_by(book_id=book_id).first()
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'book not found'},404

api.add_resource(BooksView, '/books')
api.add_resource(BookView,'/book/<book_id>')

app.debug = True
if __name__ == '__main__':
    app.run(host='localhost', port=5002)