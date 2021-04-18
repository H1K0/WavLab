from WavZard import WavZard
from MatHero import db
from math import sin, asin, tan, atan, pi
from numpy import array as arr, ndarray, zeros, hstack as seq, vectorize as npfunc
from collections.abc import Callable as Func


class SounDier:
    """So, here we go working with the sound."""

    def __init__(self, wav: WavZard) -> None:
        self.wavfile = wav
        self.channels = self.wavfile.channels
        self.bitdepth = self.wavfile.bitdepth
        self.samprate = self.wavfile.samprate

    @property
    def peak(self) -> float:
        return 2 ** (self.bitdepth - 1) - 1

    def wave(self, freq: float, form: str = 'sine', offset: float = 0) -> Func[[float], float]:
        """Generates the basic wave function (amp=1) with `freq` frequency and `form` form (defaults to 'sine') for `soundier`.
        Phase offset can also be given (in periods).

        Supported types: 'sine', 'triangle', 'saw', 'square'."""
        freq /= self.samprate
        offset /= freq
        if form == 'sine':
            return lambda s: sin(freq * 2 * pi * (s + offset))
        elif form == 'triangle':
            return lambda s: 2 / pi * asin(sin(2 * pi * freq * (s + offset)))
        elif form == 'saw':
            return lambda s: -2 / pi * atan(tan(pi * freq * (s + 0.5 / freq + offset)))
        elif form == 'square':
            return lambda s: -round(freq * (s + offset) % 1) * 2 + 1
        else:
            raise ValueError(f'unexpected form \'{form}\'')

    def sine(self, freq: float, amp: float, dur: float, offset: float = 0) -> ndarray:
        """Generates sine wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs and
        `offset` phase offset (in periods)."""
        return arr([self.peak * amp * self.wave(freq, 'sine', offset)(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def triangle(self, freq: float, amp: float, dur: float, offset: float = 0) -> ndarray:
        """Generates triangle wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs and
        `offset` phase offset (in periods)."""
        return arr([self.peak * amp * self.wave(freq, 'triangle', offset)(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def saw(self, freq: float, amp: float, dur: float, offset: float = 0) -> ndarray:
        """Generates saw wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs and
        `offset` phase offset (in periods)."""
        return arr([self.peak * amp * self.wave(freq, 'saw', offset)(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def square(self, freq: float, amp: float, dur: float, offset: float = 0) -> ndarray:
        """Generates square wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs and
        `offset` phase offset (in periods)."""
        return arr([self.peak * amp * self.wave(freq, 'square', offset)(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def silence(self, dur: float) -> ndarray:
        """Generates `dur` secs silence."""
        return zeros(round(dur * self.samprate), dtype=f'int{self.bitdepth}')

    def clip(self, wave: ndarray, level: float) -> ndarray:
        """Returns a clipped signal at `level` (relative)."""
        clipper = npfunc(lambda s: min(s, level * self.peak) * (s > 0) +
                                   max(s, -level * self.peak) * (s < 0), otypes=[f'int{self.bitdepth}'])
        return clipper(wave)

    def am(self, carr: ndarray, modfunc: Func[[float], float], offset: float = 0) -> ndarray:
        """Applies amplitude modulation to `carr` by `mod` function with `offset` phase offset (in samples)."""
        mod = arr([modfunc(s + offset) for s in range(len(carr))])
        return self.render(carr * mod)

    def wam(self, carr: ndarray, zero: float, amp: float, freq: float, form: str = 'sine',
            offset: float = 0) -> ndarray:
        """Applies amplitude modulation to `carr` by wave of `form` form (defaults to 'sine')
        on `zero` level with `amp` amplitude, `freq` frequency and `offset` phase offset (in periods).

        Supported waveforms: 'sine', 'triangle', 'saw', 'square'."""
        offset *= self.samprate / freq
        return self.am(carr, lambda s: zero + amp * self.wave(freq, form)(s), offset)

    def adsr(self, dur: float, att: float = .01, dec: float = .1, sus: float = 1, rel: float = .01) -> ndarray:
        """Linear ADSR envelope generator. Takes duration, attack, decay, and release in secs and relative sustain."""
        size = round(dur * self.samprate)
        env = zeros(size) + sus
        att = round(att * self.samprate)
        dec = round(dec * self.samprate)
        rel = round(rel * self.samprate)
        s = 0
        while s < min(size, att):  # attack
            env[s] = s / att
            s += 1
        while s < min(size, att + dec):  # decay
            env[s] = 1 - (s - att) * (1 - sus) / dec
            s += 1
        s = max(0, size - rel)
        while s < size:  # release
            env[s] *= 1 - (s - size + rel) / rel
            s += 1
        return env

    def glue(self, *waves: ndarray) -> ndarray:
        """Glue waves."""
        return seq(waves)

    def render(self, wave: ndarray) -> ndarray:
        """Render wave data to output format."""
        return arr(wave, dtype=f'int{self.bitdepth}')

    def write(self, *data: ndarray) -> None:
        self.wavfile.write(seq(data))


def telephone(num: str, vol: float = db(-8)) -> ndarray:
    """Convert some symbols to DTMF."""
    global sound
    num = num.upper()
    dtmf = sound.silence(.1)
    for n in num:
        this = sound.silence(.08)
        if n in ('1', '2', '3', 'A'):
            this += sound.sine(697, vol, .08)
        if n in ('4', '5', '6', 'B'):
            this += sound.sine(770, vol, .08)
        if n in ('7', '8', '9', 'C'):
            this += sound.sine(852, vol, .08)
        if n in ('*', '0', '#', 'D'):
            this += sound.sine(941, vol, .08)
        if n in ('1', '4', '7', '*'):
            this += sound.sine(1209, vol, .08)
        if n in ('2', '5', '8', '0'):
            this += sound.sine(1336, vol, .08)
        if n in ('3', '6', '9', '#'):
            this += sound.sine(1477, vol, .08)
        if n in ('A', 'B', 'C', 'D'):
            this += sound.sine(1633, vol, .08)
        dtmf = seq([dtmf, this, sound.silence(.1)])
    return dtmf
