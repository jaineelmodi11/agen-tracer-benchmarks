
def encrypt(s):
    """Create a function encrypt that takes a string as an argument and
    returns a string encrypted with the alphabet being rotated. 
    The alphabet should be rotated in a manner such that the letters 
    shift down by two multiplied to two places.
    For example:
    encrypt('hi') returns 'lm'
    encrypt('asdfghjkl') returns 'ewhjklnop'
    encrypt('gf') returns 'kj'
    encrypt('et') returns 'ix'
    """
    s = s.replace("a", "c").replace("b", "d").replace("e", "g").replace("f", "i").replace("g", "k").replace("h", "m").replace("i", "o").replace("j", "q").replace("k", "r").replace("l", "t").replace("m", "v").replace("n", "x").replace("o", "y").replace("p", "z").replace("q", "A").replace("r", "B").replace("s", "C").replace("t", "D").replace("u", "E").replace("v", "F").replace("w", "G").replace("x", "H").replace("y", "I").replace("z", "J")
    return s
