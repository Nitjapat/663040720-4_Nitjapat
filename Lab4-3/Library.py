import datetime

class LibraryItem:
    def __init__(self, title, item_id):
        self.title = title
        self._id = item_id
        self._checked_out = False
    
    def get_status(self):
        
        return "Checked out" if self._checked_out else "Available"
    
    def check_out(self):
        if not self._checked_out:
            self._checked_out = True
            return True
        return False

    
    def return_item(self):
        if self._checked_out:
            self._checked_out = False
            return True
        return False

    def display_info(self):
        print(f"Title: {self.title} | ID: {self._id} | Status: {self.get_status()}")

class Book(LibraryItem):
    def __init__(self, title, item_id, author):
        super().__init__(title, item_id)
        self.author = author
        self.pages_count = 0 
    def set_pages(self, count):
        self.pages_count = count

    def display_info(self):
        print(f"Book: {self.title} by {self.author} | {self.pages_count} pages | Status: {self.get_status()}")

class TextBook(Book):
    def __init__(self, title, item_id, author, subject, grade_level):
        super().__init__(title, item_id, author)
        self.subject = subject
        self.grade_level = grade_level

    def display_info(self):
        print(f"Textbook: {self.title} ({self.subject}, Grade {self.grade_level}) | {self.pages_count} pages | Status: {self.get_status()}")

class Magazine(LibraryItem):
    def __init__(self, title, item_id, issue_number):
        super().__init__(title, item_id)
        self.issue_number = issue_number
        
        now = datetime.datetime.now()
        self.month = now.strftime("%B")
        self.year = now.year

    def display_info(self):
        print(f"Magazine: {self.title} (Issue #{self.issue_number}) | Date: {self.month} {self.year} | Status: {self.get_status()}")


