from SounDier import SounDier
from collections.abc import Callable as Func
from numpy import ndarray


class SynthRade:
    """This guy helps you with creating simple sampler synth.
    All he need is a `SounDier` object and a waveform to be taken as a sample."""

    def __init__(self, soundier: SounDier, sample: Func[[float, float, float], ndarray]) -> None:
        self.soundier = soundier
        self.sample = sample

    def __call__(self, freq: float, vol: float, dur: float) -> ndarray:
        return self.sample(freq, vol, dur)
