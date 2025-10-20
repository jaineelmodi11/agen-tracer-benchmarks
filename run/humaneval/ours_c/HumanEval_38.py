

def encode_cyclic(s: str):
    """
    returns encoded string by cycling groups of three characters.
    """
    # split string to groups. Each of length 3.
    groups = [s[(3 * i):min((3 * i + 3), len(s))] for i in range((len(s) + 2) // 3)]
    # cycle elements in each group. Unless group has fewer elements than 3.
    groups = [(group[1:] + group[0]) if len(group) == 3 else group for group in groups]
    return "".join(groups)


def decode_cyclic(s: str):
    """
    takes as input string encoded with encode_cyclic function. Returns decoded string.
    """
    groups = s.split()
    decoded = []
    for group in groups:
        if len(group) % 3 != 0:
            raise ValueError("Group must have a multiple of 3 elements")
        middle = int(len(group) / 3)
        start = group[:middle]
        end = group[middle:]
        decoded.append(start + end)
    return " ".join(decoded)

    # Test cases
    print(encode_cyclic("abcde"))  # Should print "abxyz"
    print(decode_cyclic("abxyz"))  # Should print "abcde"

    ```

    This solution includes the `encode_cyclic` and `decode_cyclic` functions, which are designed to handle cyclic encoding and decoding of strings based on their cyclic nature. The provided test cases demonstrate
