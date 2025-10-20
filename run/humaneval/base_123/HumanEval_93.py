
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
    # Create an empty string to hold the encoded message
    encoded_message = ""

    # Iterate through each character in the input message
    for char in message:
        if char.isalpha():
            # Check if the character is a vowel
            if char.lower() in "aeiou":
                # Find the index of the next vowel
                next_vowel_index = (ord(char) - ord("a") + 1) % 26
                # Replace the current vowel with the next one
                encoded_message += chr(ord(char) - 3)
            else:
                # If not a vowel, just keep the original character
                encoded_message += char

    return encoded_message

    # Test cases to verify the correctness of the solution
    print(encode
