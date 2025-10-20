
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
    num = 2

    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1

    return primes


    # Test cases to verify correctness
    print(count_up_to(5)) # Expected output: [2, 3]
    print(count_up_to(11)) # Expected output: [2, 3, 5, 7]
    print(count_up_to(0)) # Expected output: []
    print(count_up_to(20)) # Expected output: [2, 3, 5, 7, 11, 13, 17, 19]
    print(count_up_to(1)) # Expected output: []
    print(count_up_to(18))
