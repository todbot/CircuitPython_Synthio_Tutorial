
## Synthio Tutorial: Modulation

<!--ts-->
   * [Synthio Tutorial: Modulation](#synthio-tutorial-modulation)
      * [About Envelopes](#about-envelopes)
      * [About LFOs](#about-lfos)
         * [LFO scale &amp; offset](#lfo-scale--offset)
         * [LFO waveform](#lfo-waveform)
         * [LFO resolution](#lfo-resolution)
         * [Making waveforms with ulab.numpy](#making-waveforms-with-ulabnumpy)
      * [Vibrato: Add LFO to pitch](#vibrato-add-lfo-to-pitch)
      * [Tremolo: Add LFO to amplitude](#tremolo-add-lfo-to-amplitude)
      * [Fade in LFO](#fade-in-lfo)
      * [Bend-in pitch envelope](#bend-in-pitch-envelope)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Tue Mar 25 10:24:08 PDT 2025 -->

<!--te-->

Modulation is the automation of changing a parameter over time in a synthesizer.
It adds "liveliness" to a sound without you needing to be tweaking parameters by hand.

In `synthio` there are two types of modulators:

- [`Envelope`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Envelope)
   – a one-shot series of timed stages ("ADSR"), only for volume, ranges from 0.0 to 1.0, updated every sample
- [`LFO`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.LFO)
   – a (usually) cycling pattern that can affect most `synthio` parameters, by default ranges from -1.0 to 1.0, updated every 256 samples (puts a limit on fastest LFO we can have)

The `synthio` LFO modulation system is very rich, offering a set of [`MathOperations`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.MathOperation)
to let you combine an LFO with other LFOs or other parameters in your code.

### About Envelopes

The simplest modulation tool in `synthio` is the amplitude envelope, aka `synthio.Envelope`.
Unlike other synthesis systems, `Envelope` can only be used for the amplitude envelope,
i.e. either `synth.envelope` (amp envelope for all notes) or `note.envelope` parameter
(per-note amp envelope). For other case where we might use an envelope,
like a pitch envelope or filter envelope, we must instead use one-shot LFOs.

In our [`synth_setup.py`](./1_getting_started/synth_setup.py) file, we set up a default
amplitude envelope that works for most of the example:

```py
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)
```
This sets the amplitude envelope for all notes played on that synth.
`synthio.Envelope` has these parameters:

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

Here's an example of showing how to use an Envelope.  Notice that an Envelope's parameters
are read-only once created.
Use the knobs to play around with different attack and release times to get different effects:

```py
# 2_modulation/code_envelope.py
import time, random
import synthio
from synth_setup import synth, knobA, knobB
while True:
    synth.envelope = synthio.Envelope(
        attack_level = 0.8, sustain_level = 0.8,
        attack_time = 2 * (knobA.value/65535),  # range from 0-2 seconds
        release_time = 2 * (knobB.value/65535),  # range from 0-2 seconds
        )
    midi_note = random.randint(48,60)
    synth.press(midi_note)
    time.sleep(synth.envelope.attack_time)  # wait enough time to hear the attack finish
    synth.release(midi_note)
    time.sleep(synth.envelope.release_time)  # wait enough time to hear the release finish
```
> [2_modulation/code_envelope.py](./2_modulation/code_envelope.py)

```
[ ... TBD video of code_envelope.py TBD ... ]
```


### About LFOs

Low-frequency oscillators ("LFOs") are common in sound synthesis as a way of automating
the "knob twiddling" one might physically do to a parameter on a synthesizer.
Common uses of LFOs are for vibrato and tremolo effects.


#### LFO scale & offset

In `synthio`, the default LFO waveform is a triangle wave ranging from -1.0 to 1.0,
centered around zero.  You can change that range with `LFO.scale`.
And with `LFO.offset`, the waveform doesn't have to be centered around zero.
Some examples of synthio LFOs:

```py
lfo1 = synthio.LFO(scale=0.3)  # ranges from -0.3 to +0.3
lfo2 = synthio.LFO(offset=100)  # ranges from 99 to 101
lfo2 = synthio.LFO(offset=1500, scale=500)   # ranges from 1000 to 2000
```

In the last example the LFO to ranges between 1000 and 2000, but we specify it with
offset=1500 and scale=500. That is, `offset` acts as the midpoint of the range
and `scale` is how much above and below that midpoint to move.

Instead of midpoint/range, we sometimes want to think of an LFO ranging from a
min/max.  To turn min/max to midpoint/range, use a function like this:

```py
def lfo_set_min_max(lfo, lmin=0.0, lmax=1.0):
    """Set an LFO's mininum and maximum values, for default LFO waveform"""
    lfo.scale = (lmax - lmin)/2
    lfo.offset = lmax - lfo.scale
```
Thinking of LFOs in terms of min/max will be very helpful when dealing with filters later.
This function only applies to the default -1/+1 triangle wave; if you load up your
own LFO waveform, the `.scale` and `.offset` functions will work a bit differently.


#### LFO waveform

The default waveform of `LFO` is a zero-centered triangle wave that goes 0 -> +1 -> 0 -> -1 -> 0.
What if we want a different action? We can do that by setting `LFO.waveform`.
Since `LFO` smoothly interpolates between the values we provide in our waveform,
we can supply the smallest possible waveform of two numbers, like this:

```py
import synthio
import ulab.numpy as np

# create a positive-only triangle wave
lfo_positive = synthio.LFO(rate=0.5, waveform=np.array([0,32767], dtype=np.int16))
```

A few things to note:

- `LFO.waveform` expects a list of signed 16-bit numbers, which it turns into a floating-point
value between -1 and +1.  From the above example, 32767 corresponds to +1 (and 32768 would be -1)

- We only need to specify two numbers as `synthio.LFO` will smoothly interpolate them for us.

- `LFO` interpolates the last value back to the first value, so after the LFO goes from 0 to 32767,
it will interpolate back down to 0 on the loop of the LFO.
One would expect that `[0,32767]` would make a sawtooth and `[0,32767,0]` would make a triangle,
but that's now how `LFO` works.
To make a sawtooth wave, you need to specify a larger waveform with something like,
`synthio.LFO(rate=0.5, waveform=np.linspace(0, 32767, num=128, dtype=np.int16))`

- The min/max discussion and code above changes if we specify a different waveform.
For the positive-only waveform shown, its range is 1 instead of 2, so min/max calculations should remove the /2.

- Note we're using `ulab.numpy` to actually create the waveforms.

#### LFO resolution

Internally, the LFO waveform is stored as signed 16-bit numbers (-32768 to +32767),
which gets exposed to Python as -1 to +1. Thus LFOs have lower resolution
that real CircuitPython floating point numbers.  This is normally not an issue.
But it does mean that while you can use a waveform like
`LFO(waveform=np.array([100,200],dtyp=np.int16))`,
the result will be "steppier" than doing `LFO(offset=150,scale=100)`.
The latter uses the full 16-bit range available to `LFO`.


#### Making waveforms with `ulab.numpy`

When dealing with waveforms, the [`ulab.numpy`](https://docs.circuitpython.org/en/latest/shared-bindings/ulab/numpy/index.html) library
([Learn Guide](https://learn.adafruit.com/ulab-crunch-numbers-fast-with-circuitpython/ulab-numpy-phrasebook),
[ulab book](https://micropython-ulab.readthedocs.io/en/latest/ulab-intro.html))
is very handy as it's designed to operate on large lists of numbers.
It's based on [`numpy`](https://numpy.org/doc/stable/reference/arrays.html), so one
can often find `numpy` tips that work with `ulab.numpy`.

For `synthio`, the most useful part is the basic creation of numpy arrays, with functions like:
- `np.array([0,1,2,3], dtype=np.int16)`
  -- create a 4-element numpy array of 16-bit signed integers with the contents of the Python list
- `np.linspace(-100, 100, num=50, dtype=np.int16)`
  -- create a 50-element numpy array of 16-bit signed integers, ranging from -100 to 100

Any numpy array of `dtype=np.int16` can be used as a `synthio.LFO` waveform or a `synthio.Note.waveform`.

### Vibrato: Add LFO to pitch

To give the notes some "motion", let's add pitch vibrato to them with an LFO.
Vibrato is a slight "warble" in a note's pitch.
In `synthio`, instead of sending MIDI note numbers to `synth.press()`, we need to start
creating [`synthio.Note`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Note)
objects
so we can access per-note properties, like the `note.bend` property.

The `note.bend` property will bend the note's frequency up an octave with a +1 input and
down an octave with a -1 input. Attaching a default LFO that ranges from -1 to 1
will cause a vibrato that's two octaves wide, way too intense.  Instead, we can set
`scale = 1/12` to only scale up and down a semitone, but I like only a single semitone of vibrato,
so `scale = 0.5 * 1/12`.

Alternatively, you can uncomment the knobA line and have knobA control the scale and get really crazy.

```py
# 2_modulation/code_vibrato.py
import time, random
import synthio
from synth_setup import synth, knobA

while True:
    midi_note = random.randint(48,72)   # pick a new random note
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    bend_lfo = synthio.LFO(rate=7, scale=(1/12)*0.5)  # 7 Hz at 1 semitones warble
    note.bend = bend_lfo
    # note.bend.scale = 1 * (knobA.value/65535)  # knob controls vibrato depth up to an octave
    synth.press(note) # start note playing
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.5)
```
> [2_modulation/code_vibrato.py](./2_modulation/code_vibrato.py)

```
[ ... TBD video of code_synth_vibrato.py TBD ... ]
```

### Tremolo: Add LFO to amplitude

Another common effect is tremolo, the regular varying of a note's loudness.
This is can be done with an LFO too.  Let's also adjust the "strength" of the
tremolo effect with a knob, so as the knob is turned clockwise, the tremolo effect
gets stronger.

```py
# 2_modulation/code_tremolo.py
import time, random
import synthio
from synth_setup import synth, knobA

def lfo_set_min_max(lfo, lmin=0.0, lmax=1.0):
    lfo.scale = (lmax - lmin)/2
    lfo.offset = lmax - lfo.scale

while True:
    midi_note = random.randint(48,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.amplitude = synthio.LFO(rate=5)

    knobA_val = 1 - (knobA.value / 65535)  # convert 0-65535 to 1-0
    lfo_set_min_max(note.amplitude, knobA_val, 1)  # knob controls minimum

    synth.press(note)
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.2)
```
> [2_modulation/code_tremolo.py](./2_modulation/code_tremolo.py)

```
[ ... TBD video of code_synth_tremolo.py TBD ... ]
```

<!--
Instead we can use another `synthio` feature: [`synthio.Math`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Math) and [`synthio.MathOperation`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.MathOperation).
These are a collection of common 3-input, 1-output tools that operate on LFOs and that
operate at LFO update speeds in the background, so we don't have to write Python to
copy a value from an LFO, modify it, then write it to what the LFO is modifying.
Think of it as a generalization of the `.scale` & `.offset` features of LFO.
-->


### Fade in LFO

If we want to "automate the automation" of turning the knob to increase and decrease
the strength of the tremolo LFO, we can use another `synthio` feature to combine two LFOs:
[`synthio.Math`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Math) and [`synthio.MathOperation`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.MathOperation).
`MathOperations` are a collection of common 3-input, 1-output tools that operate on LFOs via `Math`.
They operate at LFO update speeds in the background, so we don't have to write Python to
copy a value from an LFO, modify it, then write it to what the LFO is modifying.

In the case of fading in the tremolo effect, we can do that with a one-shot ramp-up LFO.

```py
# 2_modulation/code_tremolo_fadein.py
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

fadein_lfo = synthio.LFO(rate=1, once=True, waveform=np.array([0,32767], dtype=np.int16)))
tremolo_lfo = synthio.LFO(rate=5, scale=0.5, offset=0.5)

fadein_tremolo_lfo = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                  1,
                                  tremolo_lfo,
                                  fadein_lfo)

while True:
    midi_note = random.randint(48,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.amplitude = fadein_tremolo_lfo
    synth.press(note)
    for i in range(50):
        print(note.amplitude.value)
        time.sleep(0.05)
    #time.sleep(5)
    synth.release(note)
    time.sleep(1)
```
> [2_modulation/code_tremolo_fadein.py](./2_modulation/code_tremolo_fadein.py)

```
[ ... TBD video of code_synth_tremolo_fadein.py TBD ... ]
```

### Bend-in pitch envelope

Many instruments when played don't hit their target pitch immediately.
Guitar strings, for instance, start a little sharp when struck before settling
down to their pitch.  Horn players often "bend-up" into a note to hit their pitch.

We approximate that in synthesizers with an envelope on pitch.
For bend-up or bend-in, we can use our "fade-in" LFO from our previous example,
but applied directly to the `note.bend` property.

```py
# 2_modulation/code_bendin.py
import time, random
import synthio
from synth_setup import synth, knobA

while True:
    midi_note = random.randint(48,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    bend_rate = 0.1
    bend_amount = 1
    bendin_lfo = synthio.LFO(once=True, rate=bend_rate, scale=bend_amount,
                            waveform=np.array([0,32767], dtype=np.int16)))
    note.bend = bendin_lfo

    synth.press(note)
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.2)


```
