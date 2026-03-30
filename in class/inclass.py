from abc import ABC, abstractmethod

class DigitalProduct(ABC):
    product_counter = 0

    def __init__(self, title, price):
        self.title = title
        self.price = price
        DigitalProduct.product_counter += 1
        self.product_ID = 1000 + DigitalProduct.product_counter

    @abstractmethod
    def calc_download_size(self):
        """Calculate download size in MB."""
        pass

    @abstractmethod
    def calc_delivery_time(self):
        """Calculate delivery time in minutes."""
        pass

    def gen_download_link(self):
        return f"domain.com/download/{self.product_ID}"


class Ebook(DigitalProduct):
    def __init__(self, title, price, num_pages, format="PDF"):
        super().__init__(title, price)
        self.num_pages = num_pages
        self.format = format

    def calc_download_size(self):
        return self.num_pages * 0.1

    def calc_delivery_time(self):
        return 1 + (self.num_pages / 100)


class VideoGame(DigitalProduct):
    def __init__(self, title, price, genre, required_storage):
        super().__init__(title, price)
        self.genre = genre
        self.required_storage = required_storage 

    def calc_download_size(self):
        return self.required_storage

    def calc_delivery_time(self):
        return 5 + (self.required_storage / 1000) * 2

#Testing Code

print("--- TESTING EBOOK ---")
my_ebook = Ebook("Python Mastery", 29.99, 500, "PDF")

print(f"Product: {my_ebook.title} (ID: {my_ebook.product_ID})")
print(f"Price: ${my_ebook.price}")
print(f"Download Link: {my_ebook.gen_download_link()}")
print(f"Size: {my_ebook.calc_download_size()} MB") 
print(f"Delivery Time: {my_ebook.calc_delivery_time()} mins") 


print("\n--- TESTING VIDEO GAME ---")
my_game = VideoGame("Space Explorer", 59.99, "Sci-Fi", 5000) 

print(f"Product: {my_game.title} (ID: {my_game.product_ID})")
print(f"Price: ${my_game.price}")
print(f"Download Link: {my_game.gen_download_link()}")
print(f"Size: {my_game.calc_download_size()} MB")
print(f"Delivery Time: {my_game.calc_delivery_time()} mins")