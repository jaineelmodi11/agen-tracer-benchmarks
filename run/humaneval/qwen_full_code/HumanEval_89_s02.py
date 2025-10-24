
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
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shifted_alphabet = alphabet[2:] + alphabet[:2]
    result = ""
    for char in s:
        if char.isalpha():
            index = alphabet.index(char.lower())
            new_index = (index + 2 * 2) % 26
            new_char = shifted_alphabet[new_index]
            result += new_char.upper() if char.isupper() else new_char
        else:
            result += char
    return result
