
CircuitPython Synthio Tutorial
==============================

Version: 0.1 - 4 Apr 2024

Welcome to a CircuitPython Synthio Tutorial.

In CircuitPython, `synthio` is a built-in module for doing sound synthesis
on microcontrollers such as the Pico (RP2040/RP2350) and ESP32.
This guide will focus on a Pico RP2040 and PCM5102a I2S DAC,
but it applies to [any board that supports `synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#module-synthio).

The repo for this tutorial lives at [https://github.com/todbot/CircuitPython_Synthio_Tutorial](https://github.com/todbot/CircuitPython_Synthio_Tutorial) where you can download
[all the code as a zip file](https://github.com/todbot/CircuitPython_Synthio_Tutorial/archive/refs/heads/main.zip).

## Who this guide is for

This tutorial assumes you know some Python and [CircuitPython](https://circuitpython.org) already.
It doesn't try to assume you know much about [synthesizers](https://www.youtube.com/watch?v=cWslSTTkiFU) or [music theory](https://www.youtube.com/watch?v=rgaTLrZGlk0),
but of course, knowing the basics of ["subtractive synthesis"](https://en.wikipedia.org/wiki/Subtractive_synthesis) will help understand
how `synthio` works and how it differs from that standard.

## What this guide is

This guide hopes to show how `synthio` "thinks" about sound synthesis,
show techniques for implementing common synthesis concepts with `synthio`,
and provide useful code snippets to help make new synth things in CircuitPython.


## How this guide is structured

This guide is broken up into multiple sections. Each section focuses on a topic,
and will use techniques and terms discussed in previous sections.

Every example code block is a fully working program, no code snippets here, with
download links to ready-to-run code.
Some functionality will be provided by external libraries or an included script
(most notably [`synth_setup.py`](./1_getting_started/synth_setup.py)).

Each example code block also exists as a `code_[name].py` file that can be copied to
your device's CIRCUITPY drive as `code.py` to run.  The file will sometimes
contain extra explanatory comments or print statements that will be elided
in this guide.

Each example (with a few exceptions) will do something sonically interesting by
itself, but also have a bit of interactivity with the knobs and button.  So even
if you don't have the knobs & button wired up, you should still get a sense of
what the example is about.

## Sections


### [1. Getting Started](./README-1-Getting-Started.md)
-- Going from a fresh Pico to making boops and responding to inputs

### [2. Modulation](./README-2-Modulation.md)
-- Making those boops sound more alive with LFOs and Envelopes

### [3. Filters](./README-3-Filters.md)
-- How to use synthio's filters and modulate them

### [4. Oscillators and Wavetables](./README-4-Oscillators-Wavetables.md)
-- Change a note's waveform, at any time, even use WAVs

### [5. MIDI](./README-5-MIDI.md)
-- How to respond to MIDI messages (velocity, pitchbend, CCs) in synthio

### [6. Audio Effects](./README-6-Audio-Effects.md)
-- Using the `audiofilters` and `audiodelays` modules to add effects

### [7. Synth Voice](./README-7-Synth-Voice.md)
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

I and others have created several projects and libraries that use `synthio`.
Some are listed here:

* todbot: [circuitpython-syntho-tricks](https://github.com/todbot/circuitpython-synthio-tricks)
* todbot: [pico_test_synth](https://github.com/todbot/pico_test_synth)
* todbot: [qtpy_synth](https://github.com/todbot/qtpy_synth)
* todbot: [Workshop Computer](https://github.com/todbot/Workshop_Computer/tree/main/Demonstrations%2BHelloWorlds/CircuitPython)
* gamblor: [synth drum sounds](https://gist.github.com/gamblor21/15a430929abf0e10eeaba8a45b01f5a8)
* cedargrove [CircuitPython_WaveBuilder](https://github.com/CedarGroveStudios/CircuitPython_WaveBuilder)
* cedargrove: [CircuitPython_Chime](https://github.com/CedarGroveStudios/CircuitPython_Chime)
* relic-se: [PicoSynth_Sandbox](https://github.com/relic-se/PicoSynth_Sandbox/)
* relic-se: [CircuitPython_SynthVoice](https://github.com/relic-se/CircuitPython_SynthVoice), [CircuitPython_Waveform](https://github.com/relic-se/CircuitPython_Waveform), [CircuitPython_KeyManager](https://github.com/relic-se/CircuitPython_KeyManager)
