from flask import Flask, render_template, request, redirect, url_for
from library import Book, Member, Library

app = Flask(__name__)
library = Library()


# Home route
@app.route('/')
def index():
    return render_template("index.html")


# View and Add Books
@app.route('/books', methods=['GET', 'POST'])
def books():
    # Filter by availability
    show_available = request.args.get("available", "all")
    if show_available == "available":
        books = [book for book in library.get_all_books() if book['available']]
    else:
        books = library.get_all_books()

    # Add new book
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        publication_year = request.form['publication_year']
        isbn = request.form['isbn']
        new_book = Book(title, author, publication_year, isbn)
        library.add_book(new_book)
        return redirect(url_for('books'))

    return render_template("books.html", books=books, show_available=show_available)


# Search for Books
@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '').lower()
    results = []
    if query:
        results = [
            book for book in library.get_all_books()
            if query in book['title'].lower() or query in book['author'].lower() or query in book['isbn']
        ]
    return render_template("search.html", query=query, results=results)


# View and Register Members
@app.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        name = request.form['name']
        member_id = request.form['member_id']
        new_member = Member(name, member_id)
        library.register_member(new_member)
        return redirect(url_for('members'))
    return render_template("members.html", members=library.get_all_members())


# Borrow Book
@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_isbn = request.form['book_isbn']
        library.lend_book(member_id, book_isbn)
        return redirect(url_for('books'))
    return render_template("borrow.html", members=library.get_all_members(), books=library.get_all_books())


# Return Book
@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        member_id = request.form['member_id']
        book_isbn = request.form['book_isbn']
        library.return_book(member_id, book_isbn)
        return redirect(url_for('books'))
    return render_template("return.html", members=library.get_all_members(), books=library.get_all_books())


# Run the application
if __name__ == '__main__':
    app.run(debug=True)