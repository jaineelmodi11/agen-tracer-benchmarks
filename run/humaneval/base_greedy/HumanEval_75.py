
def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    # Check if the number is less than 100
    if a < 100:
    # Check if the number is divisible by 2, 3, and 5
    if a % 2 == 0 and a % 3 == 0 and a % 5 == 0:
        return True
    # Check if the number is divisible by 2, 3, and 7
    elif a % 2 == 0 and a % 3 == 0 and a % 7 == 0:
        return True
    # Check if the number is divisible by 2, 5, and 7
    elif a % 2 == 0 and a % 5 == 0 and a % 7 == 0:
        return True
    # Check if the number is divisible by 3, 5, and 7
    elif a % 3 == 0 and a % 5 == 0 and a % 7 == 0:
        return True
    # If none of the above conditions are met, return False
    else:
        return False
    else:
    return False
