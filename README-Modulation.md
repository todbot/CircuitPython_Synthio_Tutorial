
##
## Synthio Tutorial: Modulation

<!--ts-->
   * [Synthio Tutorial: Modulation](#synthio-tutorial-modulation)
      * [About LFOs](#about-lfos)
      * [Vibrato: Add LFO to pitch](#vibrato-add-lfo-to-pitch)
      * [Tremolo: Add LFO to amplitude](#tremolo-add-lfo-to-amplitude)
      * [Controlling "strength" of LFO](#controlling-strength-of-lfo)
      * [Fade in LFO](#fade-in-lfo)
      * [Envelope, for amplitude](#envelope-for-amplitude)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Wed Mar 12 09:28:13 PDT 2025 -->

<!--te-->

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
