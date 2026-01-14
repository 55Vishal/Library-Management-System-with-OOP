import json
import os
from datetime import datetime, timedelta
from libraryManagementSystem import Book, Member, Library

def test_book_class():
    """Test Book class functionality"""
    print("Testing Book class...")

    # Create a book
    book = Book("Test Book", "Test Author", "1234567890", 2023)
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.isbn == "1234567890"
    assert book.year == 2023
    assert book.available == True
    print("✓ Book creation successful")

    # Test check_out
    success, msg = book.check_out("MEM001")
    assert success == True
    assert book.available == False
    assert book.borrowed_by == "MEM001"
    assert book.due_date is not None
    print("✓ Book check_out successful")

    # Test return_book
    success, msg = book.return_book()
    assert success == True
    assert book.available == True
    assert book.borrowed_by is None
    assert book.due_date is None
    print("✓ Book return successful")

    # Test to_dict and from_dict
    book_dict = book.to_dict()
    assert book_dict['title'] == "Test Book"
    new_book = Book.from_dict(book_dict)
    assert new_book.title == book.title
    print("✓ Book serialization successful")

def test_member_class():
    """Test Member class functionality"""
    print("\nTesting Member class...")

    # Create a member
    member = Member("John Doe", "MEM001")
    assert member.name == "John Doe"
    assert member.member_id == "MEM001"
    assert member.borrowed_books == []
    print("✓ Member creation successful")

    # Test borrow_book
    success, msg = member.borrow_book("1234567890")
    assert success == True
    assert "1234567890" in member.borrowed_books
    print("✓ Member borrow successful")

    # Test return_book
    success, msg = member.return_book("1234567890")
    assert success == True
    assert "1234567890" not in member.borrowed_books
    print("✓ Member return successful")

    # Test max books limit
    for i in range(5):
        member.borrow_book(f"ISBN{i}")
    success, msg = member.borrow_book("ISBN6")
    assert success == False
    assert "Maximum borrow limit" in msg
    print("✓ Max borrow limit enforced")

    # Test to_dict and from_dict
    member_dict = member.to_dict()
    assert member_dict['name'] == "John Doe"
    new_member = Member.from_dict(member_dict)
    assert new_member.name == member.name
    print("✓ Member serialization successful")

def test_library_class():
    """Test Library class functionality"""
    print("\nTesting Library class...")

    # Create library
    library = Library()
    assert isinstance(library.books, dict)
    assert isinstance(library.members, dict)
    print("✓ Library creation successful")

    # Add book
    book = Book("Library Book", "Lib Author", "1111111111")
    success, msg = library.add_book(book)
    assert success == True
    assert "1111111111" in library.books
    print("✓ Add book successful")

    # Register member
    member = Member("Jane Doe", "MEM002")
    success, msg = library.register_member(member)
    assert success == True
    assert "MEM002" in library.members
    print("✓ Register member successful")

    # Borrow book
    success, msg = library.borrow_book("MEM002", "1111111111")
    assert success == True
    assert library.books["1111111111"].available == False
    assert "1111111111" in library.members["MEM002"].borrowed_books
    print("✓ Borrow book successful")

    # Return book
    success, msg = library.return_book("MEM002", "1111111111")
    assert success == True
    assert library.books["1111111111"].available == True
    assert "1111111111" not in library.members["MEM002"].borrowed_books
    print("✓ Return book successful")

    # Search books
    results = library.search_books("Library", "title")
    assert len(results) == 1
    assert results[0].title == "Library Book"
    print("✓ Search books successful")

    # Test statistics
    stats = library.get_statistics()
    assert stats['total_books'] == 1
    assert stats['total_members'] == 1
    print("✓ Statistics successful")

def test_file_operations():
    """Test file save/load operations"""
    print("\nTesting file operations...")

    # Create test data
    library = Library()
    book = Book("File Test Book", "File Author", "2222222222")
    member = Member("File Member", "MEM003")
    library.add_book(book)
    library.register_member(member)

    # Save data
    success, msg = library.save_data()
    assert success == True
    assert os.path.exists('books.json')
    assert os.path.exists('members.json')
    print("✓ Save data successful")

    # Load data in new library instance
    new_library = Library()
    success, msg = new_library.load_data()
    assert success == True
    assert len(new_library.books) == 1
    assert len(new_library.members) == 1
    assert "2222222222" in new_library.books
    assert "MEM003" in new_library.members
    print("✓ Load data successful")

    # Clean up test files
    if os.path.exists('books.json'):
        os.remove('books.json')
    if os.path.exists('members.json'):
        os.remove('members.json')
    print("✓ File cleanup successful")

