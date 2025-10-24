
def cycpattern_check(a , b):
    """You are given 2 words. You need to return True if the second word or any of its rotations is a substring in the first word
    cycpattern_check("abcd","abd") => False
    cycpattern_check("hello","ell") => True
    cycpattern_check("whassup","psus") => False
    cycpattern_check("abab","baa") => True
    cycpattern_check("efef","eeff") => False
    cycpattern_check("himenss","simen") => True

    """
    """Check if any rotation of the second word is a substring in the first word."""
    # Concatenate the second word with itself to handle rotations
    concatenated_word = b + b
    # Check if the first word contains any rotation of the second word
    return any(concatenated_word[i:] == a for i in range(len(b) + 1))
