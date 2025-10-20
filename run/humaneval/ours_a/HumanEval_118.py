
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
    for i in range(len(word) - 1):
        if word[i] not in vowels and word[i + 1] not in vowels:
            return word[i]
    return ""

    # Check function with provided data points
    print(get_closest_vowel("yogurt"))  # Expected output: "u"
    print(get_closest_vowel("FULL"))    # Expected output: "U"
    print(get_closest_vowel("quick"))   # Expected output: ""
    print(get_closest_vowel("ab"))      # Expected output: ""import re
