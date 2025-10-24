
def exchange(lst1, lst2):
    """In this problem, you will implement a function that takes two lists of numbers,
    and determines whether it is possible to perform an exchange of elements
    between them to make lst1 a list of only even numbers.
    There is no limit on the number of exchanged elements between lst1 and lst2.
    If it is possible to exchange elements between the lst1 and lst2 to make
    all the elements of lst1 to be even, return "YES".
    Otherwise, return "NO".
    For example:
    exchange([1, 2, 3, 4], [1, 2, 3, 4]) => "YES"
    exchange([1, 2, 3, 4], [1, 5, 3, 4]) => "NO"
    It is assumed that the input lists will be non-empty.
    """
    # Your code here
    # Check if all elements in lst1 are even
    if all(num % 2 == 0 for num in lst1):
        # Check if all elements in lst2 are even
        if all(num % 2 == 0 for num in lst2):
            return "YES"
        else:
            return "NO"
    else:
        return "NO"

    # Test cases
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4]))  # Should return "YES"
    print(exchange([1, 2, 3, 4], [1, 5, 3, 4]))  # Should return "NO"
    print(exchange([1, 2, 3, 4], [2, 4, 6, 8]))  # Should return "YES"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 5]))  # Should return "NO"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4, 5]))  # Should return "YES"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4, 5, 6]))  # Should return "NO"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7]))  # Should return "YES"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8]))  # Should return "NO"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9]))  # Should return "YES"
    print(exchange([1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))  # Should return "NO"
    print(exchange([1, 2, 3, 4], [1, 2,
