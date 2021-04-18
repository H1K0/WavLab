from math import log10 as lg


def db(val: float) -> float:
    """Converts dB to multiplier."""
    return 10 ** (val / 20)


def diatonic(note: str) -> float:
    """Returns the frequency for given diatonic note. 'A5' is 440 Hz."""
    note = note.lower()
    st = 0
    if note[:2] in ('c#', 'db'):
        st -= 8
        note = note[2:]
    elif note[:2] in ('d#', 'eb'):
        st -= 6
        note = note[2:]
    elif note[:2] in ('f#', 'gb'):
        st -= 3
        note = note[2:]
    elif note[:2] in ('g#', 'ab'):
        st -= 1
        note = note[2:]
    elif note[:2] == 'a#':
        st += 1
        note = note[2:]
    elif note[0] == 'c':
        st -= 9
        note = note[1:]
    elif note[0] == 'd':
        st -= 7
        note = note[1:]
    elif note[0] == 'e':
        st -= 5
        note = note[1:]
    elif note[0] == 'f':
        st -= 4
        note = note[1:]
    elif note[0] == 'g':
        st -= 2
        note = note[1:]
    elif note[0] == 'a':
        note = note[1:]
    elif note[0] == 'h':
        st += 2
        note = note[1:]
    elif note[0] == 'b':
        st += 1
        note = note[1:]
    st += 12 * (int(note) - 5)
    return 440 * 2 ** (st / 12)


def rel(val: float, peak: float, digs: int = 0) -> str:
    if val == 0:
        return '-inf'
    return str(round(20 * lg(abs(val) / peak), digs))
