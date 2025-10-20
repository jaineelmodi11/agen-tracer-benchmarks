
def select_words(s, n):
    """Given a string s and a natural number n, you have been tasked to implement 
    a function that returns a list of all words from string s that contain exactly 
    n consonants, in order these words appear in the string s.
    If the string s is empty then the function should return an empty list.
    Note: you may assume the input string contains only letters and spaces.
    Examples:
    select_words("Mary had a little lamb", 4) ==> ["little"]
    select_words("Mary had a little lamb", 3) ==> ["Mary", "lamb"]
    select_words("simple white space", 2) ==> []
    select_words("Hello world", 4) ==> ["world"]
    select_words("Uncle sam", 3) ==> ["Uncle"]
    """
    # Remove non-alphabetic characters and convert to lowercase
    cleaned_s = re.sub(r'[^a-zA-Z]', '', s).lower()

    # Split the cleaned string into words
    words = cleaned_s.split()

    # Filter words with exactly n consonants
    filtered_words = [word for word in words if len(re.findall('(?i)[bcdfghjklmnpqrstvwxyz][^bcdfghjklmnpqrstvwxyz]', word)) == n]

    return filtered_words
