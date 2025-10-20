
def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..


    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """
    # Your code here
    for i in range(1, len(lst), 2):
        if lst[i] % 2 == 0:
            lst.append(lst[i])
    return lst

    print(add([4, 2, 6, 7]))


    # def remove(lst):
    #     """Given a non-empty list of integers lst. remove all odd numbers from it.

    #     Examples:
    #         remove([3, 5, 8, 9, 10, 11, 12, 13, 14, 15]) ==> [3, 5, 9, 11, 13, 15]
    #         remove([1, 2, 3, 4
