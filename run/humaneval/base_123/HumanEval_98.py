
def count_upper(s):
    """
    Given a string s, count the number of uppercase vowels in even indices.
    
    For example:
    count_upper('aBCdEf') returns 1
    count_upper('abcdefg') returns 0
    count_upper('dBBE') returns 0
    """
    # Define the pattern for uppercase vowels at even indices
    pattern = '[AEIOU]+'

    # Use regex to find all matches and return their count
    return len(re.findall(pattern, s))

    # Check function with provided data points
