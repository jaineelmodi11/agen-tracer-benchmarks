
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
    # Check for empty string
    if not txt:
    return []

    # Check for spaces or commas
    if ' ' in txt or ',' in txt:
    # Split by space
    return txt.split()
    else:
    # Count lowercase letters with odd alphabetical order
    count = sum(1 for char in txt if ord(char) - ord('a') % 2
