
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
    # Check if there are enough odd numbers in lst1 to swap with the even numbers in lst2
    num_odd_in_lst1 = sum(1 for i in lst1 if i % 2 != 0)

    # Check if there are enough even numbers in lst2 to swap with the odd numbers in lst1
    num_even_in_lst2 = sum(1 for j in lst2 if j % 2 == 0)

    # If both conditions are met, return "YES", otherwise return "NO"
    return 'YES' if (num_odd_in_lst1 >= len(lst2) or num_even_in_lst2 >= len(lst1)) else 'NO'

    # Example usage
    print(exchange([1, 2, 3,
