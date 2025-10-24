
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
    # Sort the array based on the length of the numbers
    arr.sort(key=lambda x: len(str(x)))

    # Reverse the sorted array
    arr.reverse()

    # Replace each digit by its corresponding name
    return [name[0] if num.isdigit() else 'One' for num, name in zip(arr, ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine'])] 

    # Test cases
    print(by_length([3, 1, 2, 5, 0]))  # Output: ['Five', 'One', 'Two', 'Three', 'Nine']
    print(by_length([2, 1, 2, 1]))    # Output: ['One', 'Two', 'Two', 'One']
    print(by_length([4, 1, 3, 4, 0]))  # Output: ['Four', 'One', 'Three', 'One', 'Nine']
    print(by_length([1, 2, 3, 4, 3, 2, 1]))  # Output: ['Three', 'Two', 'One', 'One', 'Two', 'Three', 'One']
    print(by_length([]))  # Output: []
    print(by_length([1, 2, 3, 4, 5, 6, 7, 8, 9]))  # Output: ['Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two', 'One']
    print(by_length([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))  # Output: ['Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two', 'One', 'One']
    print(by_length([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]))  # Output: ['Nine', 'Eight', 'Seven', 'Six', 'Five', 'Four', 'Three', 'Two', 'One', 'One', 'One']
    print(by_length([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]))  # Output: ['
