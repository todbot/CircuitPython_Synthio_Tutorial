
CircuitPython Synthio Tutorial
==============================

Version: 0.4 - 23 Apr 2025

Welcome to a CircuitPython Synthio Tutorial.

In CircuitPython, [`synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/)
is a built-in module for doing sound synthesis
on microcontrollers.
This guide focuses on using `synthio` with the [Raspberry Pico RP2040 and Pico 2 RP2350](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
with an [PCM5102a I2S DAC](https://todbot.com/blog/2023/05/16/cheap-stereo-line-out-i2s-dac-for-circuitpython-arduino-synths/)
for audio output, but applies to other microcontrollers that [support `synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/support_matrix.html?filter=synthio)
(like ESP32) and other audio output techniques (like [`PWMOut`](https://docs.circuitpython.org/en/latest/shared-bindings/pwmio/index.html#pwmio.PWMOut) and
analog [`AudioOut`](https://docs.circuitpython.org/en/latest/shared-bindings/audioio/index.html)).

The main URL for this tutorial is:
[https://todbot.github.io/CircuitPython_Synthio_Tutorial/](https://todbot.github.io/CircuitPython_Synthio_Tutorial/)
Its repo is [https://github.com/todbot/CircuitPython_Synthio_Tutorial](https://github.com/todbot/CircuitPython_Synthio_Tutorial) where you can download
[all the code as a zip file](https://github.com/todbot/CircuitPython_Synthio_Tutorial/archive/refs/heads/main.zip).


## What this guide is

This guide hopes to show how [`synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/)
"thinks" about sound synthesis,
showing techniques for implementing common synthesis concepts with `synthio`.
This guide provides over 50 complete CircuitPython example programs (with a [video for each one](https://www.youtube.com/playlist?list=PLW9arycjoILj7l4WvLYqQbdK9b_ZYYPxy))
that show different aspects of `synthio`, acting as a starting point for your own explorations
and combinining them into new synth devices.

This guide will focus on a Pico RP2040 and PCM5102a I2S DAC,
but it applies to [any board that supports `synthio`](https://docs.circuitpython.org/en/latest/shared-bindings/support_matrix.html?filter=synthio).
All code will work unchanged on a Pico 2 (RP2350) and soem code will *only* work on
the RP2350.


## Who this guide is for

This tutorial assumes you know some Python and [CircuitPython](https://circuitpython.org) already.
It doesn't try to assume you know much about [synthesizers](https://www.youtube.com/watch?v=cWslSTTkiFU) or [music theory](https://www.youtube.com/watch?v=rgaTLrZGlk0),
Of course, knowing the basics of ["subtractive synthesis"](https://en.wikipedia.org/wiki/Subtractive_synthesis) will help understand
more what `synthio` is doing and how it differs from that standard.


## How this guide is structured

This guide is broken up into multiple sections. Each section focuses on a topic,
and will use techniques and terms discussed in previous sections.

Every example code block is a fully working program, no code snippets here, with
download links to ready-to-run code. After each code block, is a [demo video](https://www.youtube.com/playlist?list=PLW9arycjoILj7l4WvLYqQbdK9b_ZYYPxy)
showing the code in action.
Some functionality will be provided by external libraries or included scripts
(most notably [`synth_setup.py`](./1_getting_started/synth_setup.py)).

Each example code block in the guide also exists as a `code_[name].py` file
that can be copied to your device's CIRCUITPY drive as `code.py` to run.
The file will sometimes contain extra explanatory comments or print statements.
Almost every example also has an accompanying video to let you hear and see
what it's doing.

Every example (hopefully) does something sonically interesting just sitting there,
and most will also have a bit of interactivity with the knobs and button.
So even if you don't have the knobs & button wired up, you should still get a sense of
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


## Changelog

- 0.4 - 23 Apr 2025 - added video examples for Section 4, changed to embeds
- 0.3 - 21 Apr 2025 - added video examples for Section 3
- 0.2 - 14 Apr 2025 - added video examples for Section 1 & 2
- 0.1 - 4 Apr 2025 - initial release for review
