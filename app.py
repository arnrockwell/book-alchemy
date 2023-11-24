from flask import Flask, redirect, render_template, request, url_for
from data_models import db, Author, Book
from api import get_cover

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'
db.init_app(app)

# Create the tables
# with app.app_context():
#   db.create_all()

@app.route("/")
def home():
  books = Book.query.all()

  return render_template("home.html", books=books, get_cover=get_cover)


""" Sort book info by title in descending order """
@app.route("/title/desc")
def sort_by_title_desc():
  books = Book.query.order_by(Book.title.desc()).all()

  return render_template("home.html", books=books, get_cover=get_cover)


""" Sort book info by title in ascending order """
@app.route("/title/asc")
def sort_by_title_asc():
  books = Book.query.order_by(Book.title.asc()).all()

  return render_template("home.html", books=books, get_cover=get_cover)


""" Sort book info by author in descending order """
@app.route("/author/desc")
def sort_by_author_desc():
  books = Book.query.join(Author).order_by(Author.name.desc()).all()

  return render_template("home.html", books=books, get_cover=get_cover)


""" Sort book info by author in ascending order """
@app.route("/author/asc")
def sort_by_author_asc():
  books = Book.query.join(Author).order_by(Author.name.asc()).all()

  return render_template("home.html", books=books, get_cover=get_cover)


""" Search for a book using a word or phrase """
@app.route("/search", methods=["GET", "POST"])
def search_books():
  if request.method == "POST":
    phrase = request.form.get("search")
    results = Book.query.filter(Book.title.like(f'%{phrase}%')).all()

  return render_template("search.html", results=results, get_cover=get_cover, author_id=results.author_id)


""" Add new author to the database """
@app.route("/add_author", methods=["GET", "POST"])
def add_author():
  message = None

  if request.method == "POST":
    name = request.form.get("name")
    birth_date = request.form.get("birthdate")
    date_of_death = request.form.get("date_of_death")

    new_author = Author(name, birth_date, date_of_death)
    db.session.add(new_author)
    db.session.commit()

    message = "New author successfully added!"

    return redirect(url_for("home", message=message))

  return render_template("add_author.html")


""" Update an existing author in the database """
@app.route("/author/<int:author_id>/edit", methods=["GET", "POST"])
def edit_author(author_id):
  message = None

  author = Author.query.get(author_id)

  if request.method == "POST":
    name = request.form.get("name")
    birth_date =  request.form.get("birthdate")
    date_of_death = request.form.get("date_of_death")

    author.name = name
    author.birth_date = birth_date
    author.date_of_death = date_of_death
    db.session.commit()

    message = "Author successfully updated!"

    return redirect(url_for("home", message=message))

  return render_template("edit_author.html", author=author)


""" Delete an author from the database """
@app.route("/author/<int:author_id>/delete", methods=["GET", "POST"])
def delete_author(author_id):
  message = None

  author = Author.query.get(author_id)

  if request.method == "POST":
    db.session.delete(author)
    db.session.commit()

    message = "Author successfully deleted!"

    return redirect(url_for("home", message=message))

  return render_template("delete_author.html", author=author)


""" Add new book to the database """
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
  message = None

  if request.method == "POST":
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    publication_year = request.form.get("publication_year")

    find_author = Author.query.filter_by(name=author).first()

    if find_author is None:
      message = "Author not found. Please try again."

    else:
      author_id = find_author.id

      new_book = Book(isbn, title, author_id, publication_year)
      db.session.add(new_book)
      db.session.commit()

      message = "New book successfully added!"

      return redirect(url_for("home", message=message))

  return render_template("add_book.html")


""" Edit an existing book in the database """
@app.route("/book/<int:book_id>/edit", methods=["GET", "POST"])
def edit_book(book_id):
  message = None

  book = Book.query.get(book_id)

  if request.method == "POST":
    isbn = request.form.get("isbn")
    title = request.form.get("title")
    author = request.form.get("author")
    publication_year = request.form.get("publication_year")

    find_author = Author.query.filter_by(name=author).first()

    if find_author is None:
      message = "Author not found. Please try again."

    else:
      author_id = find_author.id

      book.isbn = isbn
      book.title = title
      book.author_id = author_id
      book.publication_year = publication_year
      db.session.commit()

      message = "Book Successfully updated!"

      return redirect(url_for("home", message=message))

  return render_template("edit_book.html", book=book)


""" Delete a book from the database """
@app.route("/book/<int:book_id>/delete", methods=["GET", "POST"])
def delete_book(book_id):
  message = None

  book = Book.query.get(book_id)
  author_count = Book.query.filter_by(author_id=book.author_id).count()

  if request.method == "POST":
    if author_count == 1:
      author = Author.query.get(book.author_id)
      db.session.delete(author)

    db.session.delete(book)
    db.session.commit()

    message = "Book successfully deleted!"

    return redirect(url_for("home", message=message))

  return render_template("delete_book.html", book=book, get_cover=get_cover)


if __name__ == "__main__":
  # Launch flask server
  app.run(host='0.0.0.0', port=5000, debug=True)
