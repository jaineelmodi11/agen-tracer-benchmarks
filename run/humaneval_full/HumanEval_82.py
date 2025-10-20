
def prime_length(string):
    """Write a function that takes a string and returns True if the string
    length is a prime number or False otherwise
    Examples
    prime_length('Hello') == True
    prime_length('abcdcba') == True
    prime_length('kittens') == True
    prime_length('orange') == False
    """
    """Check if the length of the string is a prime number."""
    # Calculate the length of the string
    length = len(string)

    # Check if the length is a prime number
    return length > 1 and all(length % i != 0 for i in range(2, int(math.sqrt(length)) + 1))
