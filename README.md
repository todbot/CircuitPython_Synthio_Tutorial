

CircuitPython Synthio Tutorial
==============================

<!--ts-->
* [CircuitPython Synthio Tutorial](#circuitpython-synthio-tutorial)
   * [Getting Started](#getting-started)
      * [Wiring up](#wiring-up)
         * [With a breadboard](#with-a-breadboard)
         * [Using the pico_test_synth PCB](#using-the-pico_test_synth-pcb)
      * [Code setup](#code-setup)
   * [Make a Sound](#make-a-sound)
      * [Hello boop!](#hello-boop)
      * [Simple test, with buffer and organized](#simple-test-with-buffer-and-organized)
   * [Modulation](#modulation)
      * [Add LFO to pitch](#add-lfo-to-pitch)
      * [Add LFO to amplitude](#add-lfo-to-amplitude)
      * [Controlling "strength" of LFO](#controlling-strength-of-lfo)
      * [Fade in LFO](#fade-in-lfo)
   * [Filters](#filters)
      * [Add a filter](#add-a-filter)
      * [Changing filter parameters by hand](#changing-filter-parameters-by-hand)
      * [Add LFO to a filter](#add-lfo-to-a-filter)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Sat Mar  8 17:21:04 PST 2025 -->

<!--te-->

##
## Getting Started
##

### Wiring up

The examples in this tutorial will use the following components:

- 1 x Raspberry Pi Pico RP2040 or compatible
- 1 x PCM5102 I2S DAC module or similar
- 2 x 10k potentiometer
- 1 x tact switch button

But these examples will work with just about any board/chip that has
CircuitPython `synthio` support and some sort of audio output,
like a [QTPy RP2040 with PWM output](https://github.com/todbot/qtpy_synth).


#### With a breadboard

A quick way of assembling the above components is with a solderless breadboard.
This is a great way to get started, but breadboard connections can become
intermittent, making them frustrating.

<img src="./docs/synthio_tutorial_wiring1.png" width=400/>


#### Using the pico_test_synth PCB


### Code setup

- [Install CircuitPython for Pico](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)
as normal.

- Considering [installing circup](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup/install-circup) to make adding libraries easier

- Use your editor of choice to edit the There are many

##
## Make a Sound


### Hello boop!

Let's test out the wiring.  Create a `code.py` file
on the CIRCUITPY drive with the contents of the
[`code_helloboop.py`](./1_getting_started/code_helloboop.py) shown below.

This example makes a beep with random pitches every 0.5 seconds.
It uses the square-wave waveform that's built-in to `synthio`.

```py
# 1_getting_started/code_helloboop.py
import time
import random
import board
import synthio
import audiobusio

# how we have our circuit wired up or pico_test_synth
i2s_bck_pin = board.GP20
i2s_lck_pin = board.GP21
i2s_dat_pin = board.GP22

# hook up external stereo I2S audio DAC board
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)
# make the synthesizer
synth = synthio.Synthesizer(sample_rate=44100, channel_count=2)
# plug synthesizer into audio output
audio.play(synth)

midi_note = 60  # midi note to play, 60 = C4

while True:
    print("boop!")
    synth.press(midi_note) # start note playing
    time.sleep(0.1)
    synth.release(midi_note) # release the note we pressed
    time.sleep(0.4)
    midi_note = random.randint(32,72)   # pick a new random note
```

Note that in the above code:
- The I2S DAC requires three pins. On the Pico RP2040, the "bit_clock"
and "word_select" pins must be adjacent.
- The `Synthesizer` requires a sample_rate (44,100 is "CD-quality") and a
"channel_count". I2S is stereo, so channel_count=2.
- You "plug" the synth into the audio output to allow the synth to be heard.
- To start a sound, use `synth.press()`.
This takes either a MIDI note number from 0-127 or a `synthio.Note()`.

This sounds like:

[ .. insert code1a.py video here .. ]


### Simple test, with buffer and organized

There is an issue with the above code however.
With the synth plugged directly into the audio output, there's very little buffer
for the CPU to compute samples. It's also hard to change the overall volume of
the synth. The solution to both issues is to plug an `audiomixer` in between.

This means the audio setup goes from this:

```py
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)
synth = synthio.Synthesizer(sample_rate=44100, channel_count=2)
audio.play(synth)  # plug synth directly into audio output
```
to this:

```py
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)
mixer = audiomixer.Mixer(sample_rate=SAMPLE_RATE, channel_count=2, buffer_size=BUFFER_SIZE)
synth = synthio.Synthesizer(sample_rate=SAMPLE_RATE, channel_count=2)
audio.play(mixer)  # plug mixer into the audio output
mixer.voice[0].play(synth)  # plug synth into mixer's first 'voice'
```

Also, to make it easier to see what's different each time,
let's pull out all that setup and [put it into a new file called
`synth_setup.py`](./1_getting_started/synth_setup.py).

Our [`code.py`](./1_getting_started/synth_setup.py) now looks like the below.
We'll use this technique going forward.

```py
# 1_getting_started/code_synth_setup.py
import time, random
# run the setup and get a synth
from synth_setup import synth

midi_note = 60  # midi note to play, 60 = C4

while True:
    print("boop!")
    synth.press(midi_note) # start note playing
    time.sleep(0.2)
    synth.release(midi_note) # release the note we pressed, notice it keeps sounding
    time.sleep(0.5)
    midi_note = random.randint(32,72)   # pick a new random note
```

And this sounds like:

[ .. insert video of code_]

The sleep times have been sped up, so you can hear the notes overlapping more.
Also note there's been a special change at the end of `synth_setup.py` to make
the boops more appealing. More on that later.

### Fun with boops


##
## Modulation

### Add LFO to pitch

### Add LFO to amplitude

### Controlling "strength" of LFO

### Fade in LFO

##
## Filters


something something

### Add a filter

### Changing filter parameters by hand

### Add LFO to a filter
