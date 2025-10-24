
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
    def is_vowel(char):
    return char.lower() in 'aeiou'

    def find_closest_vowel(word):
    for i in range(len(word) - 1, -1, -1):
        if is_vowel(word[i]):
            left_consonant = word[i-1]
            right_consonant = word[i+1]
            if is_vowel(left_consonant) and is_vowel(right_consonant):
                return word[i]
    return ""

    return find_closest_vowel(word)
