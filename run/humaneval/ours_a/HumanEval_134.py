
def check_if_last_char_is_a_letter(txt):
    '''
    Create a function that returns True if the last character
    of a given string is an alphabetical character and is not
    a part of a word, and False otherwise.
    Note: "word" is a group of characters separated by space.

    Examples:
    check_if_last_char_is_a_letter("apple pie") ➞ False
    check_if_last_char_is_a_letter("apple pi e") ➞ True
    check_if_last_char_is_a_letter("apple pi e ") ➞ False
    check_if_last_char_is_a_letter("") ➞ False 
    '''
    # Check if the string is empty or only contains spaces
    if len(txt) <= 1 or txt[0] == ' ':
    return False

    # Get the last character
    last_char = txt[-1]

    # Check if the last character is a letter
    if not last_char.isalpha():
    return False

    # Check if the last character is not part of a word
    for char in txt:
    if char.isalpha() and char
