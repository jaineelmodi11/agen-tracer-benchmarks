
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
    # Splitting the text based on spaces or commas
    if ' ' in txt:
        return [word.strip() for word in txt.split()]
    elif ',' in txt:
        return len([ord(char) - ord('a') for char in txt if char.islower()])
    else:
        return len([ord(char) - ord('a') for char in txt if ord(char) >= ord('a') and ord(char) <= ord('z')])

    # Check function to verify the correctness of the solution
