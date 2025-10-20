
def get_max_triples(n):
    """
    You are given a positive integer n. You have to create an integer array a of length n.
        For each i (1 ≤ i ≤ n), the value of a[i] = i * i - i + 1.
        Return the number of triples (a[i], a[j], a[k]) of a where i < j < k, 
    and a[i] + a[j] + a[k] is a multiple of 3.

    Example :
        Input: n = 5
        Output: 1
        Explanation: 
        a = [1, 3, 7, 13, 21]
        The only valid triple is (1, 7, 13).
    """
    # Initialize result counter
    res = 0

    # Iterate over all possible values for i
    for i in range(1, n+1):
        # Calculate the sum of the current triplet
        sum_triplet = i * i - i + 1

        # Check if the sum is divisible by 3
        if sum_triplet % 3 == 0:
            # Increment the result counter
            res += 1

    return res


    # Test cases
    print(get_max_triples(5))  # Expected output: 1
    print(get_max_triples(6))  # Expected output: 2
    print(get_max_triples(8))  # Expected output: 4
    ```

    This solution iterates through all possible
