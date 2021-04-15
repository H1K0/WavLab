from WavZard import Wav
from MatHero import db
from math import sin, pi
from numpy import array as arr, hstack as seq


class SounDier:
    """So, here we go working with the sound."""
    def __init__(self, wav):
        self.wavfile = wav
        self.channels = self.wavfile.channels
        self.bitdepth = self.wavfile.bitdepth
        self.samprate = self.wavfile.samprate

    def sine(self, freq, amp, dur):
        return arr([int(amp * 2 ** (self.bitdepth - 1) * sin(2 * freq * pi * i / self.samprate))
                    for i in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def silence(self, dur):
        return arr([0 for _ in range(round(dur * self.samprate))], dtype=f'int{self.bitdepth}')

    def write(self, *data):
        self.wavfile.write(seq([*data]))


def telephone(num,vol=db(-8)):
    """Convert some symbols to DTMF."""
    global sound
    num=num.upper()
    dtmf=sound.silence(.1)
    for n in num:
        this=sound.silence(.08)
        if n in ('1','2','3','A'):
            this+=sound.sine(697,vol,.08)
        if n in ('4','5','6','B'):
            this+=sound.sine(770,vol,.08)
        if n in ('7','8','9','C'):
            this+=sound.sine(852,vol,.08)
        if n in ('*','0','#','D'):
            this+=sound.sine(941,vol,.08)
        if n in ('1','4','7','*'):
            this+=sound.sine(1209,vol,.08)
        if n in ('2','5','8','0'):
            this+=sound.sine(1336,vol,.08)
        if n in ('3','6','9','#'):
            this+=sound.sine(1477,vol,.08)
        if n in ('A','B','C','D'):
            this+=sound.sine(1633,vol,.08)
        dtmf=seq([dtmf,this,sound.silence(.1)])
    return dtmf


sound = SounDier(Wav('WAV/test.wav', channels=1, bitdepth=16, samprate=44100))
sound.write(
    telephone('2281488')
)
