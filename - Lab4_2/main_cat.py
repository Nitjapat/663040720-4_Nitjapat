"663040720-4"
"Nitjapat Supanangthong"

from cat import Cat

# Showcasing how to use the Cat class
print(Cat.get_species_info())

# Create instances
cat1 = Cat("Luna", 3, "Siamese", "White/Brown")
cat2 = Cat.from_birth_year("Garfield", 2015, "Persian", "Orange")

print(f"Total cats created: {Cat.total_cats}")
print(f"Is {cat2.name} a senior? {Cat.is_senior(cat2.age)}")

# Interact with cat1
print(cat1.meow())
cat1.play(40)
print(cat1.get_status())
print(cat1.meow())

# Calculate food amount
recommended_food = Cat.calculate_healthy_food_amount(4.5)
cat1.eat(recommended_food)
print(cat1.get_status())