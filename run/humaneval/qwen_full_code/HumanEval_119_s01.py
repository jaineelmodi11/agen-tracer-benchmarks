
def match_parens(lst):
    '''
    You are given a list of two strings, both strings consist of open
    parentheses '(' or close parentheses ')' only.
    Your job is to check if it is possible to concatenate the two strings in
    some order, that the resulting string will be good.
    A string S is considered to be good if and only if all parentheses in S
    are balanced. For example: the string '(())()' is good, while the string
    '())' is not.
    Return 'Yes' if there's a way to make a good string, and return 'No' otherwise.

    Examples:
    match_parens(['()(', ')']) == 'Yes'
    match_parens([')', ')']) == 'No'
    '''
    # Count the number of opening and closing parentheses in each string
    count1 = lst[0].count('(')
    count2 = lst[1].count(')')

    # Check if the total number of opening parentheses is equal to the total number of closing parentheses
    if count1 != count2:
        return 'No'

    # If the first string has more closing parentheses than the second, swap them
    if count1 > count2:
        lst[0], lst[1] = lst[1], lst[0]

    # Check if the concatenated string is balanced
    balance = 0
    for char in ''.join(lst):
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return 'No'

    return 'Yes'
