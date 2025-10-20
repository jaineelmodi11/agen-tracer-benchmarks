
def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    # Iterate over all possible combinations of three primes
    for i in range(2, int(math.sqrt(a)) + 1):
        for j in range(i+1, int(math.sqrt(a)) + 1):
            for k in range(j+1, int(math.sqrt(a)) + 1):
                if a % i == 0 and a % j == 0 and a % k == 0:
                    return True
    return False

    # Test cases to verify the correctness of the solution
    print(is_multiply_prime(30))  # Expected output: True
    print(is_multiply_prime(60))  # Expected output: False
    print(is_multiply_prime(49))  # Expected output: False
    ```

    This code snippet defines a function
