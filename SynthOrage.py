from SynthRade import SynthRade
from MatHero import db

simplers = {
    'Soft Pluck': \
        lambda soundier: SynthRade(soundier,
                                   lambda freq, vol, dur: soundier.render(
                                       soundier.clip(soundier.sine(freq, 1, dur) *
                                                     soundier.adsr(dur, 0, .1, db(-21)), db(-18)) *
                                       db(18) * vol)
                                   ),
    'Short Pluck': \
        lambda soundier: SynthRade(soundier,
                                   lambda freq, vol, dur: soundier.render(
                                       soundier.square(freq, 1, dur) *
                                       soundier.adsr(dur, 0, .1, 0) * vol
                                   )),
    'Trisaw': \
        lambda soundier: SynthRade(soundier,
                                   lambda freq, vol, dur: soundier.render(
                                       (soundier.triangle(freq, 2 / 3, dur) + soundier.saw(freq, 2 / 3, dur)) * vol
                                   )),
}
