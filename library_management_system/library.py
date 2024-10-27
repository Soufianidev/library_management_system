class Book:
    def __init__(self, title, author, publication_year, isbn):
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn
        self.available = True

    def display_details(self):
        return {
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "isbn": self.isbn,
            "available": self.available,
        }

    def check_availability(self):
        return self.available

    def borrow_book(self):
        if self.available:
            self.available = False

    def return_book(self):
        if not self.available:
            self.available = True


class Member:
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, book):
        if book.check_availability():
            book.borrow_book()
            self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_book()
            self.borrowed_books.remove(book)

    def view_borrowed_books(self):
        return [book.display_details() for book in self.borrowed_books]


class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, book):
        self.books.append(book)

    def register_member(self, member):
        self.members.append(member)

    def lend_book(self, member_id, book_isbn):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.isbn == book_isbn), None)
        if member and book:
            member.borrow_book(book)

    def return_book(self, member_id, book_isbn):
        member = next((m for m in self.members if m.member_id == member_id), None)
        book = next((b for b in self.books if b.isbn == book_isbn), None)
        if member and book:
            member.return_book(book)

    def get_all_books(self):
        return [book.display_details() for book in self.books]

    def get_all_members(self):
        return [{"name": m.name, "member_id": m.member_id, "borrowed_books": m.view_borrowed_books()} for m in self.members]