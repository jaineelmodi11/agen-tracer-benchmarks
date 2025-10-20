
def split_words(txt):
    '''
    Given a string of words, return a list of words split on whitespace, if no whitespaces exists in the text you
    should split on commas ',' if no commas exists you should return the number of lower-case letters with odd order in the
    alphabet, ord('a') = 0, ord('b') = 1, ... ord('z') = 25
    Examples
    split_words("Hello world!") ➞ ["Hello", "world!"]
    split_words("Hello,world!") ➞ ["Hello", "world!"]
    split_words("abcdef") == 3 
    '''
    # Check for spaces or commas
    has_spaces_or_commas = any(char in ' \',.' for char in txt)

    # Count lowercase letters with odd ASCII values
    odd_ascii_count = sum(1 for char in txt if char.islower() and ord(char) % 2 != 0)

    # Return either the list of words or the count of odd
