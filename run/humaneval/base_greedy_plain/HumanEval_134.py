
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
    # Your code here
    return txt[-1].isalpha() and not any(char.isalpha() for char in txt[:-1]) 

    # Test cases
    print(check_if_last_char_is_a_letter("apple pie"))  # ➞ False
    print(check_if_last_char_is_a_letter("apple pi e"))  # ➞ True
    print(check_if_last_char_is_a_letter("apple pi e "))  # ➞ False
    print(check_if_last_char_is_a_letter(""))  # ➞ False
