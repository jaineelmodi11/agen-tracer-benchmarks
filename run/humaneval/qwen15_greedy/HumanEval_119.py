
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
    Here's a step-by-step approach to solve the problem:

    1. Count the number of opening and closing parentheses in both strings.
    2. Check if the total number of opening parentheses is equal to the total number of closing parentheses.
    3. If the total number of opening and closing parentheses is not equal, it's impossible to form a balanced string, so return 'No'.
    4. If the total number of opening and closing parentheses is equal, we need to check if we can form a balanced string by concatenating the strings in some order.
    5. We can form a balanced string if the number of opening parentheses in the first string is less than or equal to the number of closing parentheses in the second string, or vice versa.

    Here's the implementation of the function:
