
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
    vowel_map = {'a': 'd', 'e': 'f', 'i': 'j', 'o': 'p', 'u': 'v'}

    # Initialize an empty result string
    result = ''

    # Iterate over each character in the message
    for char in message:
    # Check if the character is a letter
    if char.isalpha():
        # Determine the case of the letter
        if char.isupper():
            # Swap the case of the letter
            result += char.lower()
        else:
            # Keep the case of the letter unchanged
            result += char
    else:
        # If the character is not a letter, add it as is
        result += char

    # Replace vowels with the corresponding letter
    for vowel in vowel_map:
    result = result.replace(vowel, vowel_map[vowel])

    return result
