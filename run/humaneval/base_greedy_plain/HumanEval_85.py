
def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..


    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """
    even = []
    for i in range(1, len(lst), 2):
        if lst[i] % 2 == 0:
            even.append(lst[i])
    return sum(even)# Write your code here
    # print(add([4, 2, 6, 7])) # 2
    # print(add([1, 3, 5, 7, 9])) # 10
    # print(add([1, 3, 5, 7, 9, 11])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17, 19])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27])) # 10
    # print(add([1, 3, 5, 7, 9, 11, 13, 15, 17,
