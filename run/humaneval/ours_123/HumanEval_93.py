
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
    """
    Encodes the given message by swapping the case of all letters,
    replacing vowels with the letter that appears 2 places ahead of that vowel,
    and handling only letters.
    """
    result = ''
    for char in message:
    if char.isalpha():
        # Swap case
        if char.islower():
            result += char.upper()
        else:
            result += char.lower()
        # Replace vowels
        if char in 'aeiou':
            if char in 'aeiou':
                result += chr((ord(char) - ord('a') + 2) % 26 + ord('a'))
            else:
                result += chr((ord(char) - ord('a') + 2) % 26 + ord('A'))
    else:
        result += char
    return result
