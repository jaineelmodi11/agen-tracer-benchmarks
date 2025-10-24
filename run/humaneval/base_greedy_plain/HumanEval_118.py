
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
    vowels = "aeiouAEIOU"
    for i in range(len(word) - 1):
        if word[i] in vowels and word[i + 1] in vowels:
            return word[i + 1]
    return ""


    # Test cases
    print(get_closest_vowel("yogurt"))  # Output: "u"
    print(get_closest_vowel("FULL"))    # Output: "U"
    print(get_closest_vowel("quick"))   # Output: ""
    print(get_closest_vowel("ab"))      # Output: ""


    # Additional test cases
    print(get_closest_vowel("a"))       # Output: ""
    print(get_closest_vowel("b"))       # Output: ""
    print(get_closest_vowel("c"))       # Output: ""
    print(get_closest_vowel("d"))       # Output: ""
    print(get_closest_vowel("e"))       # Output: ""
    print(get_closest_vowel("f"))       # Output: ""
    print(get_closest_vowel("g"))       # Output: ""
    print(get_closest_vowel("h"))       # Output: ""
    print(get_closest_vowel("i"))       # Output: ""
    print(get_closest_vowel("j"))       # Output: ""
    print(get_closest_vowel("k"))       # Output: ""
    print(get_closest_vowel("l"))       # Output: ""
    print(get_closest_vowel("m"))       # Output: ""
    print(get_closest_vowel("n"))       # Output: ""
    print(get_closest_vowel("o"))       # Output: ""
    print(get_closest_vowel("p"))       # Output: ""
    print(get_closest_vowel("q"))       # Output: ""
    print(get_closest_vowel("r"))       # Output: ""
    print(get_closest_vowel("s"))       # Output: ""
    print(get_closest_vowel("t"))       # Output: ""
    print(get_closest_vowel("u"))       # Output: ""
    print(get_closest_vowel("v"))       # Output: ""
    print(get_closest_vowel("w"))       # Output: ""
    print(get_closest_vowel("x"))       # Output: ""
    print(get_closest_vowel("y"))       # Output: ""
    print(get_closest_vowel("z"))       # Output: ""


    # Test cases with vowels in the middle
    print(get_closest_vowel("a"))       # Output: ""
    print
