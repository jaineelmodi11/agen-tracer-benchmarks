
def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..


    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """
    # Initialize an empty list to store the result
    result = []

    # Iterate through the list starting from index 1 (odd indices)
    for i in range(1, len(lst), 2):
    # Add the element at the current odd index to the result list
    result.append(lst[i])

    # Return the result list
    return result
