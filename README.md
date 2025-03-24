
CircuitPython Synthio Tutorial
==============================

Version: 0.0 - 21 Mar 2024

Welcome to a CircuitPython Synthio Tutorial.

In CircuitPython, `synthio` is a built-in module for doing sound synthesis
on microcontrollers such as the Pico (RP2040/RP2350) and ESP32.
This guide will focus on a Pico RP2040 and PCM5102a I2S DAC, 
but it applies to [any board that supports `synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#module-synthio).

This tutorial assumes you know a bit of Python and [CircuitPython](https://circuitpython.org) already.
It doesn't try to assume you know much about [synthesizers](https://www.youtube.com/watch?v=cWslSTTkiFU) or [music theory](https://www.youtube.com/watch?v=rgaTLrZGlk0).

The repo for this tutorial lives at [https://github.com/todbot/CircuitPython_Synthio_Tutorial](https://github.com/todbot/CircuitPython_Synthio_Tutorial) where you can download
[all the code as a zip file](https://github.com/todbot/CircuitPython_Synthio_Tutorial/archive/refs/heads/main.zip).


## How this Guide is structured

This guide is broken up into multiple sections. Each section focuses on a topic,
and will use techniques and terms discussed in the previous section.

Every example code block is a fully working program, no code snippets here, but
some functionality will be provided by external libraries or an included script
(most notable [`synth_setup.py`](./1_getting_started/synth_setup.py)).

Each code block also exists as a `code_[name].py` file that can be copied to
your device's CIRCUITPY drive as `code.py` to run.  The file will sometimes
contain extra explanatory comments or print statements.

## Sections


* [1. Getting Started](./README-1-Getting-Started.md)
-- Going from a fresh Pico to making boops and responding to inputs

* [2. Modulation](./README-2-Modulation.md)
-- Making those boops sound more alive with LFOs and Envelopes

* [3. Filters](./README-3-Filters.md)
-- How to use synthio's filters and modulate them

* [4. Oscillators and Wavetables](./README-4-Oscillators-Wavetables.md)
-- Change a note's waveform, at any time, even use WAVs

* [5. MIDI](./README-5-MIDI.md)
-- How to respond to MIDI messages (velocity, pitchbend, CCs) in synthio

* [6. Synth Voice](./README-4-Synth-Voice.md)  [tbd]
-- Buildling a full synth voice in synthio


## Examples 

Here's some simple examples using synthio showing what's possible

* [tiny_lfo_song](https://www.youtube.com/watch?v=m_ALNCWXor0) -- song with just LFOs
* [eighties_dystopia](https://www.youtube.com/watch?v=EcDqYh-DzVA) -- 80s-style miasma
* [quicky_theremin]() -- simple theremin using `touchio`
* [wavetable_midisynth](https://www.youtube.com/watch?v=CrxaB_AVQqM) -- Play wavetables with MIDI 
* [monosynth1](https://www.youtube.com/watch?v=EcDqYh-DzVA) -- MIDI-controlled thick monosynth
* [two_pot_drone_synth](https://www.youtube.com/watch?v=xEmhk-dVXqQ) -- 3-voice two-knob drone synth

## Projects using synthio

I and others have created several projects that use `synthio`.
Some are listed here:

* [circuitpython-syntho-tricks](https://github.com/todbot/circuitpython-synthio-tricks)
* [pico_test_synth](https://github.com/todbot/pico_test_synth)
* [qtpy_synth](https://github.com/todbot/qtpy_synth)
* [Workshop Computer](https://github.com/todbot/Workshop_Computer/tree/main/Demonstrations%2BHelloWorlds/CircuitPython)
