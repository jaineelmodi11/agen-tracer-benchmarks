
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
    # Define the mapping for vowels
    vowel_map = {'a': 'e', 'e': 'i', 'i': 'o', 'o': 'u'}

    # Encode the message by swapping case and replacing vowels
    encoded_message = ''.join(
    chr((ord(char) - ord('a') + ord('A')) % 26 + ord('a'))
    if char.isalpha()
    else char
    for char in message.lower()
    )

    return encoded_message
