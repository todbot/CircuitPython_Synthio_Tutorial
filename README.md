

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
      * [Simple test: getting started](#simple-test-getting-started)
      * [Simple test: with buffer](#simple-test-with-buffer)
      * [Simple test: done](#simple-test-done)
   * [Filters](#filters)
      * [Add a filter](#add-a-filter)
      * [Changing filter parameters by hand](#changing-filter-parameters-by-hand)
      * [Add LFO to a filter](#add-lfo-to-a-filter)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Fri Mar  7 14:46:04 PST 2025 -->

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


### Simple test: getting started

This simple example lets us test out the wiring.

```py
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

while True:
    print("boop!")
    synth.press(midi_note) # start note playing
    time.sleep(0.2)
    synth.release(midi_note) # release the note we pressed
    time.sleep(0.5)
    midi_note = random.randint(32,72)   # pick a new random note
```

This sounds like:


### Simple test: with buffer

There is an issue with the above code however.
With the synth plugged directly into the audio output, there's very little buffer
for the CPU to compute samples. It's also hard to change the overall volume of
the synth. The solution to both issues is to plug an `audiomixer` in between.

[code1a.py](./code/code1a.py)
```py
# code_1a.py -- Getting synthio up and running
import time
import random
import board
import synthio
import audiobusio
import audiomixer

SAMPLE_RATE = 44100   # the audio quality of our output
BUFFER_SIZE = 4096    # memory to calculate audio 

# how we have our circuit wired up or pico_test_synth
button_pins = (board.GP28,)
knob_pin = board.GP26
i2s_bck_pin = board.GP20
i2s_lck_pin = board.GP21
i2s_dat_pin = board.GP22

# hook up external stereo I2S audio DAC board
audio = audiobusio.I2SOut(bit_clock=i2s_bck_pin, word_select=i2s_lck_pin, data=i2s_dat_pin)

# add a mixer to give us a buffer
mixer = audiomixer.Mixer(sample_rate=SAMPLE_RATE, channel_count=2, buffer_size=BUFFER_SIZE)

# make the actual synthesizer
synth = synthio.Synthesizer(sample_rate=SAMPLE_RATE, channel_count=2)

# plug the mixer into the audio output
audio.play(mixer)

# plug the synth into the first 'voice' of the mixer
mixer.voice[0].play(synth)
mixer.voice[0].level = 0.25  # 0.25 usually better for headphones

# more on this later, but makes it sound nicer
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)

midi_note = 60  # midi note to play, 60 = C4

while True:
    print("boop!")
    synth.press(midi_note) # start note playing
    time.sleep(0.2)
    synth.release(midi_note) # release the note we pressed, notice it keeps sounding
    time.sleep(0.5)
    midi_note = random.randint(32,72)   # pick a new random note

```

### Simple test: done

To make it easier to see what's different each time,
let's pull out all that setup and put it into a file called
`synth_setup.py`.  Then the above code looks like this:

```py
# code.py
import time
import board
# run all the setup and get a synth
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


##
## Filters


something something

### Add a filter

### Changing filter parameters by hand

### Add LFO to a filter
