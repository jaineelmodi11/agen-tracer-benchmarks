
def encode(message):
    """
    Write a function that takes a message, and encodes in such a 
    way that it swaps case of all letters, replaces all vowels in 
    the message with the letter that appears 2 places ahead of that 
    vowel in the english alphabet. 
    Assume only letters. 
    
    Examples:
    >>> encode('test')
    'TGST'
    >>> encode('This is a message')
    'tHKS KS C MGSSCGG'
    """
    # Convert the message to lowercase
    message = message.lower()

    # Define the mapping for vowels
    vowels = "aeiou"
    vowel_map = {v: i + 1 for i, v in enumerate(vowels)}

    # Initialize an empty string to store the encoded message
    encoded_message = ""

    # Iterate through each character in the message
    for char in message:
        if char.isalpha():
            # Check if the character is a vowel
            if char in vowels:
                # Find the index of the next vowel
                next_vowel_index = (vowel_map[char] + 2) % 26
                # Replace the original vowel with the next one
                encoded_char = chr(ord(char) -
