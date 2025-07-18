import random

# 1 Initialize an empty dictionary
my_dict = {}
print("Empty dictionary:", my_dict)

# 2 Initialize a dictionary with two key/value pairs
my_dict = {
    "Joe": 1,
    "Scott": 2
}
print("Two key/value pairs:", my_dict)

# 3 Add a new key/value pair
my_dict["John"] = 3
print("Added John:", my_dict)

# 4 Check if certain keys exist in the dictionary
print("Contains 'Joe'?", "Joe" in my_dict)     # True
print("Contains 'Scott'?", "Scott" in my_dict) # True
print("Contains 'John'?", "John" in my_dict)   # True
print("Contains 'Mary'?", "Mary" in my_dict)   # False

# 5 Function to check if a dictionary is empty
def is_empty(my_dict):
    return len(my_dict) == 0

print("Is empty ({}):", is_empty({}))           # True
print("Is empty (my_dict):", is_empty(my_dict)) # False

# 6 Function to return sum of values in a dictionary
def value_sum(my_dict):
    return sum(my_dict.values())

print("Sum of values:", value_sum(my_dict))     # 6

# 7 Function to create a dictionary from a list of tuples
def make_dict(key_value_list):
    return dict(key_value_list)

key_value_list = [("Alice", 10), ("Bob", 20), ("Charlie", 30)]
created_dict = make_dict(key_value_list)
print("Created dictionary:", created_dict)

# 8 Function to encrypt a phrase using a cipher dictionary
def encrypt(phrase, cipher_dict):
    encrypted = ''.join(cipher_dict.get(char, char) for char in phrase)
    return encrypted

CIPHER_DICTIONARY = {
    "a": "m", "b": "n", "c": "o", "d": "p", "e": "q",
    "f": "r", "g": "s", "h": "t", "i": "u", "j": "v",
    "k": "w", "l": "x", "m": "y", "n": "z", "o": "a",
    "p": "b", "q": "c", "r": "d", "s": "e", "t": "f",
    "u": "g", "v": "h", "w": "i", "x": "j", "y": "k", "z": "l"
}
phrase = "hello"
encrypted_phrase = encrypt(phrase, CIPHER_DICTIONARY)
print("Encrypted phrase:", encrypted_phrase)

# 9 Function to create a decipher dictionary
def make_decipher_dict(cipher_dict):
    return {v: k for k, v in cipher_dict.items()}

DECIPHER_DICTIONARY = make_decipher_dict(CIPHER_DICTIONARY)
decrypted_phrase = encrypt(encrypted_phrase, DECIPHER_DICTIONARY)
print("Decrypted phrase:", decrypted_phrase)

# 10 Function to create a random cipher dictionary
def make_cipher_dict(alphabet):
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
random_cipher = make_cipher_dict(ALPHABET)
print("Random cipher dictionary:", random_cipher)
