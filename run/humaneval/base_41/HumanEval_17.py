from typing import List


def parse_music(music_string: str) -> List[int]:
    """ Input to this function is a string representing musical notes in a special ASCII format.
    Your task is to parse this string and return list of integers corresponding to how many beats does each
    not last.

    Here is a legend:
    'o' - whole note, lasts four beats
    'o|' - half note, lasts two beats
    '.|' - quater note, lasts one beat

    >>> parse_music('o o| .| o| o| .| .| .| .| o o')
    [4, 2, 1, 2, 2, 1, 1, 1, 1, 4, 4]
    """
        # Convert note to integer and add to beats list
        beats.append(int(note))
    else:
        # If note is not a digit, it's a note, so add its duration to beats list
        duration = 0
        for char in note:
            if char == '|':
                duration += 2
            elif char == '.':
                duration += 1
            else:
                break
        beats.append(duration)
    return beats
