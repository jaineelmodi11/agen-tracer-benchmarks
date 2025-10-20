
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
    # Check if all elements in lst1 are odd
    if not all(x % 2 != 0 for x in lst1):
    return "NO"

    # Find the first odd element in lst1
    first_odd = next((x for x in lst1 if x % 2 != 0), None)

    # If no odd element is found, return "NO" as no exchange is needed
    if first_odd is None:
    return "NO"

    # Swap the first odd element with the last even element
