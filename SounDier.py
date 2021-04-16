from WavZard import WavZard
from MatHero import db, diatonic
from SynthOrage import simplers
from math import ceil, sin, cos, pi
from numpy import array as arr, zeros, hstack as seq, vectorize as numfunc


class SounDier:
    """So, here we go working with the sound."""

    def __init__(self, wav):
        self.wavfile = wav
        self.channels = self.wavfile.channels
        self.bitdepth = self.wavfile.bitdepth
        self.samprate = self.wavfile.samprate

    @property
    def peak(self):
        return 2 ** (self.bitdepth - 1) - 1

    def wave(self, freq, form='sine'):
        """Generates the basic wave function (amp=1) with `freq` frequency and `form` form (defaults to 'sine') for `soundier`.
        Supported types: 'sine', 'triangle', 'saw', 'square'."""
        if form == 'sine':
            return lambda s: sin(freq / self.samprate * 2 * pi * s)
        elif form == 'triangle':
            return lambda s: ((-1) ** (ceil(.5 - 2 * freq / self.samprate * s) % 2) *
                              ((-(2 * freq / self.samprate * s + .5) % 1) * 2 + 1))
        elif form == 'saw':
            return lambda s: (freq / self.samprate * -s % 1) * 2 + 1
        elif form == 'square':
            return lambda s: -round(freq / self.samprate * s % 1) * 2 + 1
        else:
            raise ValueError(f'unexpected type \'{type}\'')

    def sine(self, freq, amp, dur):
        """Generates sine wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs."""
        return arr([self.peak * amp * self.wave(freq, 'sine')(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def triangle(self, freq, amp, dur):
        """Generates triangle wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs."""
        return arr([self.peak * amp * self.wave(freq, 'triangle')(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def saw(self, freq, amp, dur):
        """Generates saw wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs."""
        return arr([self.peak * amp * self.wave(freq, 'saw')(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def square(self, freq, amp, dur):
        """Generates square wave: `freq` hertz, `amp` relative amplitude (0<=[amp]<=1), `dur` secs."""
        return arr([self.peak * amp * self.wave(freq, 'square')(s)
                    for s in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def silence(self, dur):
        """Generates `dur` secs silence."""
        return zeros(round(dur * self.samprate), dtype=f'int{self.bitdepth}')

    def clip(self, wave, level):
        """Returns a clipped signal at `level` (relative)."""
        clipper = numfunc(lambda s: min(s, level * self.peak) * (s > 0) +
                                    max(s, -level * self.peak) * (s < 0), otypes=[f'int{self.bitdepth}'])
        return clipper(wave)

    def am(self, carr, modfunc, offset=0):
        """Applies amplitude modulation to `carr` by `mod` with `offset` phase offset (in samples)."""
        mod = arr([modfunc(s + offset) for s in range(len(carr))])
        return arr(carr * mod, dtype=f'int{self.bitdepth}')

    def wam(self, carr, zero, amp, freq, form='sine', offset=0):
        """Applies amplitude modulation to `carr` by wave of `form` form (defaults to 'sine') on `zero` level with `amp` amplitude, `freq` frequency and `offset` phase offset (in samples).
        Supported waveforms: 'sine', 'triangle', 'saw', 'square'."""
        return self.am(carr, lambda s: zero + amp * self.wave(freq, form)(s), offset)

    def adsr(self, dur, att=.01, dec=.1, sus=db(-3), rel=.01):
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

    def glue(self, *waves):
        """Glue waves."""
        return seq(waves)

    def render(self, wave):
        """Render wave data to output format."""
        return arr(wave, dtype=f'int{self.bitdepth}')

    def write(self, *data):
        self.wavfile.write(seq(data))


def telephone(num, vol=db(-8)):
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


if __name__ == '__main__':
    sound = SounDier(WavZard('WAV/test.wav', channels=1, bitdepth=16, samprate=44100))
    synth = simplers['Soft Pluck'](sound)
    sound.write(sound.glue(
        synth(diatonic('f#6'), 1, 5 / 4),  # an intro melody from my SPARKLE
        synth(diatonic('e6'), 1, 1 / 4),
        synth(diatonic('d6'), 1, 1 / 4),
        synth(diatonic('c#6'), 1, 7 / 4),
        synth(diatonic('d6'), 1, 1 / 4),
        synth(diatonic('e6'), 1, 1 / 4),
        synth(diatonic('h5'), 1, 5 / 4),
        synth(diatonic('a5'), 1, 1 / 4),
        synth(diatonic('c#6'), 1, 1 / 4),
        synth(diatonic('h5'), 1, 5 / 4),
        synth(diatonic('h6'), 1, 1 / 4),
        synth(diatonic('a6'), 1, 1 / 4),
        synth(diatonic('e6'), 1, 2 / 4),
        synth(diatonic('f#6'), 1, 4 / 4),
        synth(diatonic('a6'), 1, 1 / 4),
        synth(diatonic('f#6'), 1, 1 / 4),
        synth(diatonic('d6'), 1, 1 / 4),
        synth(diatonic('c#6'), 1, 7 / 4),
        synth(diatonic('d6'), 1, 1 / 4),
        synth(diatonic('e6'), 1, 1 / 4),
        synth(diatonic('h5'), 1, 4 / 4),
        synth(diatonic('h5'), 1, 1 / 4),
        synth(diatonic('a5'), 1, 1 / 4),
        synth(diatonic('c#6'), 1, 1 / 4),
        synth(diatonic('h5'), 1, 5 / 4),
    ))
