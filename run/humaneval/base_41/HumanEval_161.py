
def solve(s):
    """You are given a string s.
    if s[i] is a letter, reverse its case from lower to upper or vise versa, 
    otherwise keep it as it is.
    If the string contains no letters, reverse the string.
    The function should return the resulted string.
    Examples
    solve("1234") = "4321"
    solve("ab") = "AB"
    solve("#a@C") = "#A@c"
    """
    # Check for non-alphabetic characters and return an empty string if found
    if not any(char.isalpha() for char in s):
        return s

    # Initialize result with the first character of the input string
    res = list(s[0])

    # Iterate through each character in the string starting from the second one
    for i in range(1, len(s)):
        # Check if the current character is alphabetic
        if s[i].isalpha():
            # Reverse the case of the alphabetic character
            res[-1] = chr(ord(res[-1]) - 32)
        else:
            # Keep the alphabetic character unchanged
            res.append(s[i])

    # Join the reversed characters into a new string and return it
