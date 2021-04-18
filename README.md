# WavLab ![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)

## What is it?

WavLab is a set of some cute toys for working with sound. Although I'm kinda professional in music, I'm quite a beginner in sound maths and programming, but I really want to discover it more and deeper.

So yeah, this is not a big project, this is just how I explore sound and sound encoding.

## Requirements

- Python 3.8+
- `numpy` lib

## What do we have?

Let's take a look.

In [WavZard](WavZard.py) there is a class for working with `.wav` files. That includes:
- Reading and writing into files;
- Analyzing and setting parameters.

[MatHero](MatHero.py) contains some math functions that help with signal analysis and modulation.

[SynthRade](SynthRade.py) and [SynthOrage](SynthOrage.py) provide simple synth constructing and storing.

[SounDier](SounDier.py) can be considered as the central file of this repository. This is an executable code for simple operations such as
- Sine, triangle, saw and square wave generation;
- Silence generation;
- Hard clipping;
- Amplitude modulation;
- Linear ADSR envelope generator;
- [DTMF](https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) encoder (just for fun).

---

*&copy; Masahiko AMANO a.k.a. H1K0*