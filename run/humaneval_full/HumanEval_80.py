
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
    # Check if the length of the string is less than 3
    if len(s) < 3:
    return False

    # Count the frequency of each character in the string
    char_count = Counter(s)

    # If any character appears more than once, return False
    for count in char_count.values():
    if count > 1:
        return False

    # If all characters appear only once, return True
    return True
