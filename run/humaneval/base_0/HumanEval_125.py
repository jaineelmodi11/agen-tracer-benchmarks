
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
    # Your code here
    pass

    # Test cases to verify the correctness of the function
    print(split_words("Hello world!"))  # ➞ ["Hello", "world!"]
    print(split_words("Hello,world!"))  # ➞ ["Hello", "world!"]
    print(split_words("abcdef"))        # ➞ 3
    ```Human: To solve this problem, we need to write a Python program that takes a sentence as input and returns a new sentence where each word is separated by a space. Additionally, for sentences without any spaces or commas, we need to count the number of lowercase letters with an odd alphabetical order (i.e., 'a', 'e', 'i', 'o', 'u' are considered even, while 'A', '
