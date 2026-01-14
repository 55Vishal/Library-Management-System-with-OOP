# Library Management System with OOP

A comprehensive library management system built using Object-Oriented Programming principles in Python. This system allows librarians to manage books, members, borrowing, and returns with a user-friendly command-line interface.

## Features

- **Book Management**: Add, remove, and search books by title, author, or ISBN
- **Member Management**: Register new members and track their borrowed books
- **Borrowing System**: Check out books with automatic due date calculation
- **Return System**: Return books with overdue detection
- **Search Functionality**: Find books by various criteria
- **Data Persistence**: Save and load data using JSON files
- **Statistics**: View library statistics including total books, available books, members, and overdue items
- **User-Friendly Menu**: Interactive command-line interface for easy operation

## Classes Overview

### Book Class
- Represents a book in the library
- Attributes: title, author, ISBN, year, availability, borrowed_by, due_date, date_added
- Methods: check_out(), return_book(), is_overdue(), days_overdue(), to_dict(), from_dict()

### Member Class
- Represents a library member
- Attributes: name, member_id, borrowed_books, max_books
- Methods: borrow_book(), return_book(), to_dict(), from_dict()

### Library Class
- Manages the entire library system
- Attributes: books (dictionary), members (dictionary), data files
- Methods: add_book(), remove_book(), register_member(), borrow_book(), return_book(), search_books(), get_statistics(), save_data(), load_data()

## Installation

1. Ensure you have Python 3.6 or higher installed on your system.
2. Clone or download the project files.
3. No additional dependencies are required as the system uses only Python standard library modules.

## Usage

Run the library management system:

```bash
python libraryManagementSystem.py
```

### Menu Options

1. **Add New Book**: Add a new book to the library
2. **Register New Member**: Register a new library member
3. **Borrow Book**: Check out a book to a member
4. **Return Book**: Return a borrowed book
5. **Search Books**: Search books by title, author, or ISBN
6. **View All Books**: Display all books in the library
7. **View All Members**: Display all registered members
8. **View Overdue Books**: Show books that are past their due date
9. **Save & Exit**: Save data to files and exit
0. **Exit Without Saving**: Exit without saving changes

## File Structure

```
Library-Management-System-with-OOP/
│
├── libraryManagementSystem.py    # Main application file
├── test_library.py               # Unit tests for the system
├── README.md                     # This file
├── Problem_Statement             # Project requirements
├── books.json                    # Books data (created automatically)
└── members.json                  # Members data (created automatically)
```

## Data Persistence

The system automatically saves and loads data using JSON files:
- `books.json`: Stores all book information
- `members.json`: Stores all member information

Data is loaded when the program starts and saved when you choose to exit with saving.

## Testing

Run the unit tests to verify the system functionality:

```bash
python test_library.py
```

The tests cover:
- Book class functionality (creation, check-out, return, serialization)
- Member class functionality (borrowing, returning, limits)
- Library class functionality (management operations, search, statistics)
- File operations (save/load data)

## Sample Usage

1. Start the program
2. Add some books using option 1
3. Register members using option 2
4. Borrow books using option 3
5. Search for books using option 5
6. View statistics in the menu header
7. Save and exit using option 9

## Requirements

- Python 3.6+
- No external dependencies required



