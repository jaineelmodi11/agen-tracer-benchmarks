
def count_upper(s):
    """
    Given a string s, count the number of uppercase vowels in even indices.
    
    For example:
    count_upper('aBCdEf') returns 1
    count_upper('abcdefg') returns 0
    count_upper('dBBE') returns 0
    """
    # Define a set of uppercase vowels for easy lookup
    uppercase_vowels = {'A', 'E', 'I', 'O', 'U'}
    count = sum(1 for char in s if char.isupper() and char in uppercase_vowels)
    return count

    # Check function to verify the correctness of the solution
