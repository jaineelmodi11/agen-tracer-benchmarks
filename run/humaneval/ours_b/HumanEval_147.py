
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
    if n % 2 == 0:
        return 0

    # Initialize the result with 0
    res = 0

    # Iterate over all possible values of i
    for i in range(1, n // 2 + 1):
        # Calculate the sum of the form i^2 - i + 1
        sum_of_triplets = i**2 - i + 1
        # Check if this sum is divisible by 3
        if sum_of_triplets % 3 == 0:
            res += 1

    return res

    # Check function to verify the correctness of the solution
