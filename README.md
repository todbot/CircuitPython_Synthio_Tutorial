
CircuitPython Synthio Tutorial
==============================

Welcome to a little CircuitPython Synthio Tutorial.

In CircuitPython, `synthio` is a built-in module for doing sound synthesis
on microcontrollers such as the Pico (RP2040/RP2350).

This tutorial assumes you know a bit of Python and CircuitPython already.
It doesn't try to assume you know much about synthesizers or [music theory](https://www.youtube.com/watch?v=rgaTLrZGlk0).

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

This tutorial is broken up into sections.

* [1. Getting Started](./README-1-Getting-Started.md)
-- Going from a fresh Pico to making boops and responding to inputs

* [2. Modulation](./README-2-Modulation.md)
-- Making those boops sound more alive with LFOs and Envelopes

* [3. Filters](./README-3-Filters.md)
-- How to use synthio's filters and modulate them

* [4. Wavetables](./README-4-Wavetables.md)
-- Change a note's waveform, at any time

* [5. MIDI](./README-MIDI.md)
-- How to respond to velocity and pitchbend in synthio
