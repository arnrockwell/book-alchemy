from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
  __tablename__ = 'authors'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String)
  birth_date = db.Column(db.String)
  date_of_death = db.Column(db.String)
  book_list = db.relationship("Book", cascade="all, delete")

  def __init__(self, name, birth_date, date_of_death=None):
    self.name = name
    self.birth_date = birth_date
    self.date_of_death = date_of_death

  def __repr__(self):
    return f"Author(id={db.id}, name={db.name}, birthdate={db.birth_date})"


class Book(db.Model):
  __tablename__ = 'books'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  isbn = db.Column(db.Integer)
  title = db.Column(db.String)
  publication_year = db.Column(db.Integer)
  author_id = db.Column(db.Integer, db.ForeignKey("authors.id", ondelete="CASCADE"), nullable=False)
  author_list = db.relationship("Author", backref=db.backref("books"))

  def __init__(self, isbn, title, author_id, publication_year=None):
    self.isbn = isbn
    self.title = title
    self.publication_year = publication_year
    self.author_id = author_id

  def __repr__(self):
    return f"Book(id={db.id}, isbn={db.isbn}, title={db.title})"
