
def encrypt(s):
    """Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    For example:
    encrypt('hi') returns 'lm'
    encrypt('asdfghjkl') returns 'ewhjklnop'
    encrypt('gf') returns 'kj'
    encrypt('et') returns 'ix'
    """
    # Create a dictionary of all the characters in the alphabet
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    # Create a new list of the same length as the original string, but shifted by 2
    shifted_alphabet = alphabet[1:] + alphabet[:1]
    # Initialize a variable to hold the result
    result = ""
    # Loop through each character in the input string
    for char in s:
        if char in alphabet:
            index = alphabet.index(char)
            # Shift the index by 2
            new_index = (index + 2) % len(alphabet)
            # Add the new index to the result string
            result += shifted_alphabet[new_index]
        else:
            # If the character is not in the alphabet, add it to
