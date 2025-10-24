
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
    # Define the alphabet and the mapping for vowels
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    vowel_map = {'a': 'c', 'e': 'g', 'i': 'k', 'o': 'q', 'u': 'w', 'A': 'C', 'E': 'G', 'I': 'K', 'O': 'Q', 'U': 'W'}

    # Initialize an empty result string
    result = ''

    # Iterate over each character in the message
    for char in message:
    # Check if the character is a letter
    if char.isalpha():
        # Determine the case of the character
        if char.islower():
            # Swap the case of the character
            result += char.upper()
        else:
            # Swap the case of the character
            result += char.lower()
    else:
        # If the character is not a letter, append it as is
        result += char

    # Replace vowels with the letter that appears 2 places ahead of the vowel
    for vowel, replacement in vowel_map.items():
    result = result.replace(vowel, replacement)

    return result
