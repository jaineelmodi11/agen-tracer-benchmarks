
def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    # Check if a is less than 100
    if a < 100:
    # Iterate through possible values of the prime factors
    for i in range(2, int(a**0.5) + 1):
        if a % i == 0:
            # If any prime factor divides a, then a is not a prime number
            return False
    # If no prime factor divides a, then a is a prime number
    return True
    else:
    # If a is not less than 100, return False
