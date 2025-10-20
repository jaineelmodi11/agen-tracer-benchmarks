
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
    for i in range(len(lst1)):
        if not (lst1[i] % 2 == 0) and not (lst2[i] % 2 == 0):
            return 'NO'
    return 'YES'# This solution uses a set comprehension to check if any element in lst1 is divisible by 2. 
    # If there is at least one such element, we can't swap it with any element in lst2, so we return 'NO'.
    # Otherwise, we return 'YES'. 

    # The time complexity of this solution is O(n), where n is the length of the longer list. 
    # The space complexity is also O(n), as we are creating a new list to store the results.

    # This solution
