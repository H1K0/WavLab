from MatHero import diatonic


class SynthRade:
    """This guy helps you with creating simple sampler synth.
    All he need is a `SounDier` object and a waveform to be taken as a sample."""

    def __init__(self, soundier, sample):
        self.soundier = soundier
        self.sample = sample

    def __call__(self, freq, vol, dur):
        return self.sample(freq, vol, dur)
