
def digitSum(s):
    """Task
    Write a function that takes a string as input and returns the sum of the upper characters only'
    ASCII codes.

    Examples:
        digitSum("") => 0
        digitSum("abAB") => 131
        digitSum("abcCd") => 67
        digitSum("helloE") => 69
        digitSum("woArBld") => 131
        digitSum("aAaaaXa") => 153
    """
    """Task
    Write a function that takes a string as input and returns the sum of the upper characters only
    (ASCII codes) of the string.

    Examples:
    digitSum("") => 0
    digitSum("abAB") => 131
    digitSum("abcCd") => 67
    digitSum("helloE") => 69
    digitSum("woArBld") => 131
    digitSum("aAaaaXa") => 153
    """
    # Initialize the sum to 0
    sum = 0

    # Iterate through each character in the string
    for char in s:
    # Convert the character to its ASCII value and add it to the sum
    sum += ord(char)

    # Return the sum
    return sum
