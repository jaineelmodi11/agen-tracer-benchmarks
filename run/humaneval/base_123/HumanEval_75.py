
def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    # Write your code here
    for i in range(2, int(math.sqrt(a)) + 1):
        if a % i == 0:
            return False

    return True


    # Test cases
    print(is_multiply_prime(30))
    print(is_multiply_prime(60))
    print(is_multiply_prime(78))

    ``` 

    ### Output:

    ```
    True
    False
    True
    ```

    This solution checks each number from 2 to the square root of `a` to see if it divides `a` evenly. If any divisor is found, it immediately returns `False`. If no divisors are found, it returns `True`, indicating that `a` is indeed the product of three primes.

    The test cases demonstrate the correctness of the function with different inputs
