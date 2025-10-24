
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
    # Count the number of odd elements in lst1
    odd_count = sum(1 for num in lst1 if num % 2 != 0)

    # If there are no odd numbers, it's impossible to make all elements even
    if odd_count == 0:
    return "NO"

    # Count the number of even elements in lst2
    even_count = sum(1 for num in lst2 if num % 2 == 0)

    # If there are more even numbers than odd numbers, it's impossible to make all elements even
    if even_count > odd_count:
    return "NO"

    # If there are an equal number of odd and even numbers, we can make all elements even
    return "YES"
