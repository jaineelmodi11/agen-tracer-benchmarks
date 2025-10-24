
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
    vowels = 'aeiouAEIOU'
    result = ''

    for char in message:
        if char.isalpha():
            # Swap case
            new_char = char.swapcase()

            # Replace vowel with the next one in the alphabet
            if new_char in vowels:
                index = vowels.index(new_char)
                new_char = chr((index + 1) % 5)  # Wrap around to 'a' if necessary

            result += new_char
        else:
            result += char

    return result
