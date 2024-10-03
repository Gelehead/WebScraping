effect = "Card capacity: 1"

# Fix the case sensitivity and extract the number
card_capacity = int(effect.split("Card capacity:")[1].split()[0]) if "Card capacity:" in effect else None

print(card_capacity)