
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
    # Your code here

    # Test cases
    print(digitSum(""))  # Expected output: 0
    print(digitSum("abAB"))  # Expected output: 131
    print(digitSum("abcCd"))  # Expected output: 67
    print(digitSum("helloE"))  # Expected output: 69
    print(digitSum("woArBld"))  # Expected output: 131
    print(digitSum("aAaaaXa"))  # Expected output: 153
    ```

    This solution uses Python's built-in `ord` function to get the ASCII value of each character, then converts it back to an integer using `int`. The `sum` function is used to add up these
