"663040720-4"
"Nitjapat Supanangthong"

from datetime import datetime

class Cat:
    # 1. Class Attributes
    species = "Felis catus"
    total_cats = 0
    average_lifespan = 15

    # 2. Instance Attributes
    def __init__(self, name, age, breed, color):
        self.name = name
        self.age = age
        self.breed = breed
        self.color = color
        
        # State tracking
        self.hungry = False
        self.energy = 100
        self.happiness = 100
        
        Cat.total_cats += 1

    # 3. Instance Methods
    def meow(self):
        if self.hungry:
            return "Meeeow! (Feed me!)"
        elif self.happiness < 50:
            return "Hiss..."
        else:
            return "Purrrrr..."

    def eat(self, food_amount_g):
        print(f"{self.name} is eating {food_amount_g}g of food.")
        self.hungry = False
        self.energy = min(100, self.energy + (food_amount_g // 10))

    def play(self, play_time_mins):
        print(f"{self.name} plays for {play_time_mins} minutes.")
        self.energy = max(0, self.energy - play_time_mins)
        self.happiness = min(100, self.happiness + (play_time_mins * 2))
        if self.energy < 30:
            self.hungry = True

    def sleep(self, hours):
        print(f"{self.name} sleeps for {hours} hours.")
        self.energy = min(100, self.energy + (hours * 10))

    def get_status(self):
        return {
            "name": self.name,
            "hungry": self.hungry,
            "energy": self.energy,
            "happiness": self.happiness
        }

    # 4. Class Methods
    @classmethod
    def from_birth_year(cls, name, birth_year, breed, color):
        current_year = datetime.now().year
        age = current_year - birth_year
        return cls(name, age, breed, color)

    @classmethod
    def get_species_info(cls):
        return f"Species: {cls.species}, Average Lifespan: {cls.average_lifespan} years."

    # 5. Static Methods
    @staticmethod
    def is_senior(age):
        return age > 7

    @staticmethod
    def calculate_healthy_food_amount(weight_kg):
        return weight_kg * 20