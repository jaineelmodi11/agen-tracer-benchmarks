
def count_up_to(n):
    """Implement a function that takes an non-negative integer and returns an array of the first n
    integers that are prime numbers and less than n.
    for example:
    count_up_to(5) => [2,3]
    count_up_to(11) => [2,3,5,7]
    count_up_to(0) => []
    count_up_to(20) => [2,3,5,7,11,13,17,19]
    count_up_to(1) => []
    count_up_to(18) => [2,3,5,7,11,13,17]
    """
    primes = []
    for num in range(2, n):
        if is_prime(num):
            primes.append(num)
    return primes

    # Test cases
    print(count_up_to(5))  # Expected output: [2, 3]
    print(count_up_to(11)) # Expected output: [2, 3, 5, 7]
    print(count_up_to(0))  # Expected output: []
    print(count_up_to(20)) # Expected output: [2, 3, 5, 7, 11, 13, 17, 19]
    print(count_up_to(18)) # Expected output: [2, 3, 5, 7, 11, 13, 17]# Write a function that takes a list of integers and returns a new list containing only the even numbers from the original list.
    # Example:
    # >>> filter_evens([1, 2, 3, 4, 5, 6])
    # [2, 4, 6]
    # >>> filter_evens([10, 23, 30, 45, 56, 67])
    # [23, 45, 67]
    # >>> filter_evens([1, 3, 5, 7, 9, 11])
    # []
    # >>> filter_evens([2, 4, 6, 8, 10, 12])
    # [2, 4, 6, 8, 10]
