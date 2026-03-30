from Library import LibraryItem,Book,TextBook,Magazine

book = Book("Harry Potter", "B001", "J.K. Rowling")
print(book.get_status())  # Should print: Available
book.check_out()
print(book.get_status())  # Should print: Checked out


textbook = TextBook("Modern Physics", "T101", "Stephen Hawking", "Science", 12)
textbook.set_pages(500)
print(textbook.get_status())
textbook.display_info()
print(textbook.check_out())
print(textbook.get_status())
print("-" * 30)

magazine = Magazine("National Geographic", "M505", 452)
print(f"Issue: {magazine.issue_number} | Month: {magazine.month} | Year: {magazine.year}")
magazine.display_info()
print(magazine.check_out()) 
print(magazine.check_out())
magazine.return_item()
print(magazine.get_status()) 
print("-" * 30)