
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
      * [Fun with boops](#fun-with-boops)
         * [Generative tunes on a pentatonic scale](#generative-tunes-on-a-pentatonic-scale)
         * [Play a chord melody](#play-a-chord-melody)
      * [Controlling Notes](#controlling-notes)
         * [Controlling with buttons](#controlling-with-buttons)
         * [Controlling with MIDI](#controlling-with-midi)
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
<!-- Added by: tod, at: Mon Mar 10 14:59:49 PDT 2025 -->

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

[ image of pico_test_synth ]

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

[ .. insert code_helloboop.py video here .. ]


### Simple test, with buffer and organized

There is an issue with the above code however.
With the synth plugged directly into the audio output, there's very little buffer
for the CPU to compute samples. It's also hard to change the overall volume of
the synth. The solution to both issues is to plug an [`audiomixer`](https://docs.circuitpython.org/en/latest/shared-bindings/audiomixer/index.html)
in between.

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

Our [`code.py`](./1_getting_started/code_synth_setup.py) now looks like the below.
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

[ .. insert video of code_synth_setup here .. ]

The sleep times have been sped up, so you can hear the notes overlapping more.
Also note there's been a special change at the end of `synth_setup.py` to make
the boops more appealing. More on that later.

### Fun with boops

With just the above, we can do some fun.

#### Generative tunes on a pentatonic scale

This example uses a list of note offsets in a pentatonic scale.
Inside the `while`-loop, a random note is created from that list and played.
Since the note keeps sounding after the `synth.release()`, there are some overlap
of the notes, giving us hints of chords.  And since this is a pentatonic scale,
just about any combination of two notes sounds good together.

```py
# 1_getting_started/code_generative_penta.py
import time, random
from synth_setup import synth
root_note = 48
scale_pentatonic = (0, 2, 4, 7, 9, 12, 14, 16, 19, 21)  # two octaves of offsets

while True:
    midi_note = random.choice( [root_note+x for x in scale_pentatonic] )
    print("playing!", midi_note)
    synth.press(midi_note)
    time.sleep(0.1)
    synth.release(midi_note) # release the note we pressed, notice it keeps sounding
    time.sleep(0.2)
```

#### Play a chord melody

A similar technique lets us play a melody with chords.
In this case, we have a list of notes for our melody
(the timing between notes is still fixed)
and a list of offsets for the block chord to play based on a note.

```py
# 1_getting_started/code_chord_melody.py
import time, random
from synth_setup import synth

melody_midi_notes = (50, 55, 57, 59, 59, 59, 57, 59, 55, 55)
chord = [0,4,7]

while True:
    midi_note = melody_midi_notes[i]
    i = (i+1) % len(melody_midi_notes)
    print("playing!", midi_note)
    for n in chord: synth.press(midi_note + n)
    time.sleep(0.1)
    for n in chord: synth.release(midi_note + n)
    time.sleep(0.1)
```


### Controlling Notes

So far, the code has been triggering notes by itself.  But it's pretty easy to trigger
with keypresses or MIDI.

#### Controlling with buttons

Here's an example with physical buttons.
The `pico_test_synth` PCB has only one physical button, but with a breadboard,
you can wire up more.

The `synth_setup.py` file has been updated to have a list of button pins
and the creation of a [`keypad`](https://docs.circuitpython.org/en/latest/shared-bindings/keypad/)
"keys" object that does button debouncing and press/release events.

```py
# 1_getting_started/code_buttons.py
import synthio
from synth_setup import synth, keys
root_note = 48  # the lowest note to play

while True:
    if key := keys.events.get():
        midi_note = root_note + key.key_number  # different note for each key
        if key.pressed:
            synth.press(midi_note)
        if key.released:
            synth.release(midi_note)
```


#### Controlling with MIDI

MIDI control is very similar. Since USB MIDI is easier to set up (no extra circuitry needed),
it's shown here.  Instead of using `adafruit_midi`, the `tmidi` library is used
(available via `circup` and in the [CircuitPython Community Bundle](https://github.com/adafruit/CircuitPython_Community_Bundle/))

```py
# 1_getting_started/code_midi.py
import synthio
import usb_midi, tmidi
from synth_setup import synth, keys

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

while True:
    if msg := midi_usb.receive():
        print("midi:", msg)
        if msg.type == tmidi.NOTE_ON and msg.velocity > 0:
            synth.press(msg.note)
        elif msg.type == tmidi.NOTE_OFF or msg.velocity == 0:
            synth.release(msg.note)
```

##
## Modulation

Modulation is basically doing automated "knob-turning" of a parameter in a synthesizer.
It adds "liveliness" to a sound without you needing to be tweaking parameters by hand.

In `synthio` there are two types of modulators:

- [`Envelope`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Envelope)
   – a series of timed stages ("ADSR"), usually happening once, really only for volume, ranges from 0.0 to 1.0
- [`LFO`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.LFO)
   – a (usually) repeating pattern that can affect most any `synthio` parameter, often pitch or volume, by default ranges from -1.0 to 1.0.

The `synthio` LFO modulation system is very rich, offering a set of [`MathOperations`]() to let you combine
an LFO with other LFOs or other parameters in your code.

### About LFOs

The default LFO waveform is a triangle wave that ranges from -1.0 to 1.0.
You can change that range with `LFO.scale`.
The LFO waveform doesn't have to be centered around zero either, that can be changed
with `LFO.offset`.  Some examples of LFOs:

```py
lfo1 = synthio.LFO(scale=0.3)  # ranges from -0.3 to +0.3
lfo2 = synthio.LFO(offset=100)  # ranges from 99 to 101
lfo2 = synthio.LFO(scale=3, offset=20)   # ranges from 14 to 26  FIXME
```

I find the `scale` and `offset` way of specifying the range of an LFO confusing,
so I prefer to use one of these helper functions:

```py
def set_lfo_min_max(lfo, lmin=0.0, lmax=1.0):
    lrange = (lmax - lmin)
    lfo.scale = lrange/2
    lfo.offset = lmax - lfo.scale

def set_lfo_range_offset(lfo, lrange=2, loffset=0.0):
    lfo.scale = lrange/2
    lfo.offset = loffset + lfo.scale
```

### Vibrato: Add LFO to pitch

To give the notes some "motion", let's add pitch vibrato to them with an LFO.
In order to do that, we make a [`synthio.Note`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Note)
object and set its `note.bend` parameter.

```py
# 2_modulation/code_vibrato.py
import time, random
import synthio
from synth_setup import synth

bend_lfo = synthio.LFO(rate=7, scale=0.05)  # 7 Hz at 5%

while True:
    midi_note = random.randint(48,72)   # pick a new random note
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.bend = bend_lfo
    synth.press(note) # start note playing
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.3)
```

### Tremolo: Add LFO to amplitude

Another common effect is tremolo, the regular varying of a note's loudness.
This is easy with an LFO too.

```py
# 2_modulation/code_tremolo.py
import time, random
import synthio
from synth_setup import synth

while True:
    note = synthio.Note(synthio.midi_to_hz(midi_note))

    note.amplitude = synthio.Math(synthio.MathOperation.PRODUCT,
                                  synthio.LFO(rate=5, scale=0.1, offset=0.8), # 'a'
                                  0)  # 'b': this value we change to increase effect
    note.amplitude.b = knobA.value / 65535
    synth.press(note)
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.3)
```

### Controlling "strength" of LFO

### Fade in LFO


### Envelope, for amplitude

The simplest modulation is the amplitude envelope, something that's been already set up.
In the [`synth_setup.py`](./1_getting_started/synth_setup.py) file there is this line:

```py
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)
```
This sets the amplitude envelope for all notes played on that synth.
The amplitude envelope describes the loudness of the note over time. It has these parameters:

- `attack_time` – at the start of the note, how long to go from silence to `attack_level`
- `decay_time` – once at `attack_level`, how long to go to `decay_level`
- `sustain_level` – after the attack & decay times, the loudness to be at while the note is held
- `release_time` – once a key is released, how long for the note's sound to fade away

All `_time` values are in seconds and all `_level` values range 0.0 to 1.0.

The default settings for Envelope are:
```py
synthio.Envelope(attack_time = 0.1,
                 decay_time = 0.5,
                 release_time = 0.2,
                 attack_level = 1.0,
                 sustain_level = 0.8)
```

Some examples of amplitude envelopes you might see:
```py
# gentle rise & fall, like a string section
synth.envelope = synthio.Envelope(attack_time=1.0, release_time=1.0)

# like a plucked string
synth.envelope = synthio.Envelope(attack_time=0, decay_time=0, release_time=0.5, sustain_level=0.0 )
```


##
## Filters


something something

### Add a filter

### Changing filter parameters by hand

### Add LFO to a filter
