import json
import os
from datetime import datetime, timedelta

class Book:
    """Represents a book in the library"""

    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None
        self.date_added = datetime.now().strftime('%Y-%m-%d')

    def check_out(self, member_id, loan_period=14):
        """Check out the book to a member"""
        if not self.available:
            return False, "Book is already checked out"

        self.available = False
        self.borrowed_by = member_id
        self.due_date = (datetime.now() + timedelta(days=loan_period)).strftime('%Y-%m-%d')
        return True, f"Book checked out successfully. Due date: {self.due_date}"

    def return_book(self):
        """Return the book to the library"""
        if self.available:
            return False, "Book is already available"

        was_overdue = self.is_overdue()
        self.available = True
        self.borrowed_by = None
        self.due_date = None

        if was_overdue:
            return True, "Book returned (was overdue)"
        return True, "Book returned successfully"

    def is_overdue(self):
        """Check if the book is overdue"""
        if self.due_date and not self.available:
            due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
            return datetime.now() > due_date
        return False

    def days_overdue(self):
        """Calculate days overdue"""
        if self.is_overdue():
            due_date = datetime.strptime(self.due_date, '%Y-%m-%d')
            return (datetime.now() - due_date).days
        return 0

    def to_dict(self):
        """Convert book to dictionary for serialization"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'available': self.available,
            'borrowed_by': self.borrowed_by,
            'due_date': self.due_date,
            'date_added': self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        """Create Book instance from dictionary"""
        book = cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn'],
            year=data.get('year')
        )
        book.available = data['available']
        book.borrowed_by = data.get('borrowed_by')
        book.due_date = data.get('due_date')
        book.date_added = data.get('date_added', datetime.now().strftime('%Y-%m-%d'))
        return book

    def __str__(self):
        status = "Available" if self.available else f"Borrowed by {self.borrowed_by}"
        return f"{self.title} by {self.author} ({self.isbn}) - {status}"

class Member:
    """Represents a library member"""

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []  # List of ISBNs
        self.max_books = 5

    def borrow_book(self, isbn):
        """Borrow a book"""
        if len(self.borrowed_books) >= self.max_books:
            return False, f"Maximum borrow limit ({self.max_books}) reached"
        if isbn in self.borrowed_books:
            return False, "Book already borrowed by this member"
        self.borrowed_books.append(isbn)
        return True, "Book borrowed successfully"

    def return_book(self, isbn):
        """Return a book"""
        if isbn not in self.borrowed_books:
            return False, "Book not borrowed by this member"
        self.borrowed_books.remove(isbn)
        return True, "Book returned successfully"

    def to_dict(self):
        """Convert member to dictionary for serialization"""
        return {
            'name': self.name,
            'member_id': self.member_id,
            'borrowed_books': self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member instance from dictionary"""
        member = cls(data['name'], data['member_id'])
        member.borrowed_books = data.get('borrowed_books', [])
        return member

    def __str__(self):
        return f"{self.name} (ID: {self.member_id}) - Borrowed: {len(self.borrowed_books)} books"

class Library:
    """Manages the library system"""

    def __init__(self):
        self.books = {}  # isbn: Book
        self.members = {}  # member_id: Member
        self.books_file = 'books.json'
        self.members_file = 'members.json'
        self.load_data()

    def add_book(self, book):
        """Add a book to the library"""
        if book.isbn in self.books:
            return False, "Book with this ISBN already exists"
        self.books[book.isbn] = book
        return True, "Book added successfully"

    def remove_book(self, isbn):
        """Remove a book from the library"""
        if isbn not in self.books:
            return False, "Book not found"
        if not self.books[isbn].available:
            return False, "Cannot remove borrowed book"
        del self.books[isbn]
        return True, "Book removed successfully"

    def register_member(self, member):
        """Register a new member"""
        if member.member_id in self.members:
            return False, "Member ID already exists"
        self.members[member.member_id] = member
        return True, "Member registered successfully"

    def find_book(self, isbn):
        """Find a book by ISBN"""
        return self.books.get(isbn)

    def find_member(self, member_id):
        """Find a member by ID"""
        return self.members.get(member_id)

    def borrow_book(self, member_id, isbn):
        """Borrow a book"""
        member = self.find_member(member_id)
        if not member:
            return False, "Member not found"

        book = self.find_book(isbn)
        if not book:
            return False, "Book not found"

        success, msg = member.borrow_book(isbn)
        if not success:
            return False, msg

        success, msg = book.check_out(member_id)
        if not success:
            member.return_book(isbn)  # Rollback
            return False, msg

        return True, msg

    def return_book(self, member_id, isbn):
        """Return a book"""
        member = self.find_member(member_id)
        if not member:
            return False, "Member not found"

        book = self.find_book(isbn)
        if not book:
            return False, "Book not found"

        success, msg = member.return_book(isbn)
        if not success:
            return False, msg

        success, msg = book.return_book()
        if not success:
            member.borrow_book(isbn)  # Rollback
            return False, msg

        return True, msg

    def search_books(self, query, search_by='title'):
        """Search books by title, author, or ISBN"""
        results = []
        query = query.lower()
        for book in self.books.values():
            if search_by == 'title' and query in book.title.lower():
                results.append(book)
            elif search_by == 'author' and query in book.author.lower():
                results.append(book)
            elif search_by == 'isbn' and query in book.isbn.lower():
                results.append(book)
        return results

    def get_overdue_books(self):
        """Get list of overdue books"""
        return [book for book in self.books.values() if book.is_overdue()]

    def get_statistics(self):
        """Get library statistics"""
        total_books = len(self.books)
        available_books = sum(1 for book in self.books.values() if book.available)
        total_members = len(self.members)
        overdue_books = len(self.get_overdue_books())
        return {
            'total_books': total_books,
            'available_books': available_books,
            'total_members': total_members,
            'overdue_books': overdue_books
        }

    def save_data(self):
        """Save books and members to files"""
        try:
            with open(self.books_file, 'w') as f:
                json.dump({isbn: book.to_dict() for isbn, book in self.books.items()}, f, indent=4)
            with open(self.members_file, 'w') as f:
                json.dump({mid: member.to_dict() for mid, member in self.members.items()}, f, indent=4)
            return True, "Data saved successfully"
        except Exception as e:
            return False, f"Error saving data: {str(e)}"

    def load_data(self):
        """Load books and members from files"""
        try:
            if os.path.exists(self.books_file):
                with open(self.books_file, 'r') as f:
                    books_data = json.load(f)
                    self.books = {isbn: Book.from_dict(data) for isbn, data in books_data.items()}
            if os.path.exists(self.members_file):
                with open(self.members_file, 'r') as f:
                    members_data = json.load(f)
                    self.members = {mid: Member.from_dict(data) for mid, data in members_data.items()}
            return True, "Data loaded successfully"
        except Exception as e:
            return False, f"Error loading data: {str(e)}"

def display_menu():
    """Display the main menu"""
    print("\n" + "="*40)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("="*40)
    stats = library.get_statistics()
    print(f"Books: {stats['total_books']} (Available: {stats['available_books']})")
    print(f"Members: {stats['total_members']} | Overdue: {stats['overdue_books']}")
    print("="*40)
    print("1. Add New Book")
    print("2. Register New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View All Books")
    print("7. View All Members")
    print("8. View Overdue Books")
    print("9. Save & Exit")
    print("0. Exit Without Saving")
    print("="*40)

def add_book():
    """Add a new book"""
    title = input("Enter book title: ").strip()
    author = input("Enter author: ").strip()
    isbn = input("Enter ISBN: ").strip()
    year = input("Enter publication year (optional): ").strip()
    year = int(year) if year.isdigit() else None

    book = Book(title, author, isbn, year)
    success, msg = library.add_book(book)
    print(msg)

def register_member():
    """Register a new member"""
    name = input("Enter member name: ").strip()
    member_id = input("Enter member ID: ").strip()

    member = Member(name, member_id)
    success, msg = library.register_member(member)
    print(msg)

def borrow_book():
    """Borrow a book"""
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()

    success, msg = library.borrow_book(member_id, isbn)
    print(msg)

def return_book():
    """Return a book"""
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()

    success, msg = library.return_book(member_id, isbn)
    print(msg)

def search_books():
    """Search books"""
    print("\nSearch books by:")
    print("1. Title")
    print("2. Author")
    print("3. ISBN")
    print("4. Show all available books")

    choice = input("Enter search option: ").strip()
    if choice == '4':
        results = [book for book in library.books.values() if book.available]
        query = "available books"
    else:
        query = input("Enter search query: ").strip()
        search_by = {'1': 'title', '2': 'author', '3': 'isbn'}.get(choice)
        if not search_by:
            print("Invalid option")
            return
        results = library.search_books(query, search_by)

    print(f"\nSearch Results for '{query}':")
    print("-" * 40)
    if not results:
        print("No books found")
    else:
        for i, book in enumerate(results, 1):
            print(f"{i}. {book.title}")
            print(f"   Author: {book.author}")
            print(f"   ISBN: {book.isbn}")
            print(f"   Year: {book.year or 'N/A'}")
            status = "Available" if book.available else f"Borrowed by {book.borrowed_by}"
            if book.due_date and not book.available:
                status += f" (Due: {book.due_date})"
            print(f"   Status: {status}")
            print()
        print(f"Found {len(results)} books")

def view_all_books():
    """View all books"""
    if not library.books:
        print("No books in the library")
        return

    print("\nAll Books:")
    print("-" * 60)
    for book in library.books.values():
        print(book)
    print(f"\nTotal: {len(library.books)} books")

def view_all_members():
    """View all members"""
    if not library.members:
        print("No members registered")
        return

    print("\nAll Members:")
    print("-" * 40)
    for member in library.members.values():
        print(member)
    print(f"\nTotal: {len(library.members)} members")

def view_overdue_books():
    """View overdue books"""
    overdue = library.get_overdue_books()
    if not overdue:
        print("No overdue books")
        return

    print("\nOverdue Books:")
    print("-" * 60)
    for book in overdue:
        days = book.days_overdue()
        print(f"{book.title} by {book.author}")
        print(f"  Borrowed by: {book.borrowed_by}")
        print(f"  Due date: {book.due_date}")
        print(f"  Days overdue: {days}")
        print()

# Main program
if __name__ == "__main__":
    library = Library()
    success, msg = library.load_data()
    if success:
        print(f"Loaded {len(library.books)} books and {len(library.members)} members from file")
    else:
        print(f"Warning: {msg}")

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            register_member()
        elif choice == '3':
            borrow_book()
        elif choice == '4':
            return_book()
        elif choice == '5':
            search_books()
        elif choice == '6':
            view_all_books()
        elif choice == '7':
            view_all_members()
        elif choice == '8':
            view_overdue_books()
        elif choice == '9':
            success, msg = library.save_data()
            print(msg)
            break
        elif choice == '0':
            print("Exiting without saving...")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...")
