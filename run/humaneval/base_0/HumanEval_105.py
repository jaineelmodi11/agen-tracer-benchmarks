
def by_length(arr):
    """
    Given an array of integers, sort the integers that are between 1 and 9 inclusive,
    reverse the resulting array, and then replace each digit by its corresponding name from
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine".

    For example:
      arr = [2, 1, 1, 4, 5, 8, 2, 3]   
            -> sort arr -> [1, 1, 2, 2, 3, 4, 5, 8] 
            -> reverse arr -> [8, 5, 4, 3, 2, 2, 1, 1]
      return ["Eight", "Five", "Four", "Three", "Two", "Two", "One", "One"]
    
      If the array is empty, return an empty array:
      arr = []
      return []
    
      If the array has any strange number ignore it:
      arr = [1, -1 , 55] 
            -> sort arr -> [-1, 1, 55]
            -> reverse arr -> [55, 1, -1]
      return = ['One']
    """
    # Sort numbers between 1-9 in ascending order
    sorted_arr = sorted([i for i in range(1, 10)])

    # Reverse the sorted list
    reversed_sorted_arr = sorted_arr[::-1]

    # Replace digits with their names
    result = []
    for num in reversed_sorted_arr:
        if num == 1 or num == 4 or num == 7:
            result.append("One")
        elif num == 2 or num == 5 or num == 6:
            result.append("Two")
        elif num == 3 or num == 6:
            result.append("Three")
        elif num == 4 or num == 7:
            result.append("Four")
        elif num == 5:
