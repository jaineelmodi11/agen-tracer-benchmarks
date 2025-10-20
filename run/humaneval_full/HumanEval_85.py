
def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..


    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """
    total = 0
    for i in range(len(lst)):
    if i % 2 != 0:  # Check if the index is odd
        if lst[i] % 2 == 0:  # Check if the element is even
            total += lst[i]
    return total
