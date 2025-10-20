
def get_closest_vowel(word):
    """You are given a word. Your task is to find the closest vowel that stands between 
    two consonants from the right side of the word (case sensitive).
    
    Vowels in the beginning and ending doesn't count. Return empty string if you didn't
    find any vowel met the above condition. 

    You may assume that the given string contains English letter only.

    Example:
    get_closest_vowel("yogurt") ==> "u"
    get_closest_vowel("FULL") ==> "U"
    get_closest_vowel("quick") ==> ""
    get_closest_vowel("ab") ==> ""
    """
    vowels = 'aeiouAEIOU'
    for i, char in enumerate(word):
        if char not in vowels:
            continue
        # Find the first vowel after this one
        j = i + 1
        while j < len(word) and word[j] in vowels:
            j += 1
        # If we found a vowel before our current one, return it
        if j > i:
            return word[i:j]
    return ""


    # Test cases
    print(get_closest_vowel("yogurt"))  # Output: "u"
    print(get_closest_vowel("FULL"))     # Output: "U"
    print(get_closest_vowel("quick"))    # Output: ""
    print(get_closest_vowel("ab"))
