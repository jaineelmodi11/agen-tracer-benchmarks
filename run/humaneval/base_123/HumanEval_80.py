
def is_happy(s):
    """You are given a string s.
    Your task is to check if the string is happy or not.
    A string is happy if its length is at least 3 and every 3 consecutive letters are distinct
    For example:
    is_happy(a) => False
    is_happy(aa) => False
    is_happy(abcd) => True
    is_happy(aabb) => False
    is_happy(adb) => True
    is_happy(xyy) => False
    """
    # Check if the string has more than 2 characters
    if len(s) <= 2: 
        return False

    seen = set()

    for i in range(len(s)-2):
        if (s[i] == s[i+1]) or (s[i] == s[i+2]) or (s[i+1] == s[i+2]):
            return False

        # If any of these conditions are met, return False
        seen.add(s[i])

    return True


    # Test cases
    print(is_happy("a"))  # Expected output: False
    print(is_happy("aa"))  # Expected output: False
    print(is_happy("abcd"))  # Expected output: True
    print(is_happy("aabb
