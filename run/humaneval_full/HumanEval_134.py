
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
    # Check if the string is empty or contains only spaces
    if txt == "" or txt.strip().count(" ") == 0:
    return False

    # Get the last character
    last_char = txt[-1]

    # Check if the last character is a letter and not part of a word
    return last_char.isalpha() and (not any(char.isdigit() for char in last_char))
