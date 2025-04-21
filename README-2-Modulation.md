
# [Synthio Tutorial](.#sections): 2. Modulation

<!--ts-->
   * [About Envelopes](#about-envelopes)
   * [About LFOs](#about-lfos)
      * [LFO scale &amp; offset](#lfo-scale--offset)
      * [LFO waveform](#lfo-waveform)
      * [LFO resolution](#lfo-resolution)
      * [Making waveforms with ulab.numpy](#making-waveforms-with-ulabnumpy)
   * [Vibrato: Add LFO to pitch](#vibrato-add-lfo-to-pitch)
   * [Tremolo: Add LFO to amplitude](#tremolo-add-lfo-to-amplitude)
   * [Fade in LFO, using LERP](#fade-in-lfo-using-lerp)
   * [Bend-in pitch envelope](#bend-in-pitch-envelope)
   * [Portamento: glide between notes](#portamento-glide-between-notes)
   * [Faking Exponential Amplitude Decays with LFOs](#faking-exponential-amplitude-decays-with-lfos)
   * [Next steps](#next-steps)
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

## About Envelopes

The simplest modulation tool in `synthio` is the amplitude envelope, aka `synthio.Envelope`.
Unlike other synthesis systems, `Envelope` can only be used for the amplitude envelope,
i.e. either `synth.envelope` (amp envelope for all notes) or `note.envelope` parameter
(per-note amp envelope). Note the ramps up and down in Envelope are linear,
not logarithmic/exponential. This is easier computationally, but not always what you want
as realistic sounds usually decay in volume exponetially.

For other case where we might use an envelope,
like a pitch envelope or filter envelope, we must instead use one-shot LFOs.

In our [`synth_setup.py`](./1_getting_started/synth_setup.py) file, we set up a default
amplitude envelope that works for most of the examples:

```py
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)
```

This sets the amplitude envelope for all notes played on that synth,
while if you set `note.envelope`, it's only for that `synthio.Note` object, so
different Notes can have different envelopes.

The `synthio.Envelope` object has these parameters:

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
synth.envelope = synthio.Envelope(attack_time=0, decay_time=0, release_time=0.5, sustain_level=0.0)

# like a drum hit
synth.envelope = synthio.Envelope(attack_time=0, decay_time=0.05, release_time=0, attack_level=1, sustain_level=0)
```

Here's an example of showing how to use an Envelope.
Notice that an Envelope's parameters are read-only once created.
The `attack_time` and `release_time` are the two most common ones used.
Use the knobs to play around with different attack and release times to get different effects:

```py
# 2_modulation/code_envelope.py
import time, random
import synthio
from synth_setup import synth, knobA, knobB
while True:
    amp_env = synthio.Envelope(
        attack_level = 0.8, sustain_level = 0.8,
        attack_time = 1 * (knobA.value/65535),  # range from 0-1 seconds
        release_time = 2 * (knobB.value/65535),  # range from 0-2 seconds
    )
    synth.envelope = amp_env
    print("attack_time:%.2f release_time:%.2f" %
          (amp_env.attack_time, amp_env.release_time))
    midi_note = random.randint(48,60)
    synth.press(midi_note)
    time.sleep(amp_env.attack_time)  # wait to hear the attack finish
    synth.release(midi_note)
    # wait enough time to hear the release finish, but with some overlap
    time.sleep(max(amp_env.release_time * 0.75, 0.1))  # 0.1 sec smallest sleep
```
> [2_modulation/code_envelope.py](./2_modulation/code_envelope.py)

<a href="https://www.youtube.com/watch?v=CAu_C-53MBk" target="_blank">
<img alt="code_envelope demo" width=640 height=360
    src="https://img.youtube.com/vi/CAu_C-53MBk/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=CAu_C-53MBk)


## About LFOs

Low-frequency oscillators ("LFOs") are common in sound synthesis as a way of automating
the "knob twiddling" one might physically do to a parameter on a synthesizer.
Common uses of LFOs are for vibrato and tremolo effects.


### LFO scale & offset

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


### LFO waveform

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

### LFO resolution

Internally, the LFO waveform is stored as signed 16-bit numbers (-32768 to +32767),
which gets exposed to Python as -1 to +1. Thus LFOs have lower resolution
that real CircuitPython floating point numbers.  This is normally not an issue.
But it does mean that while you can use a waveform like
`LFO(waveform=np.array([100,200],dtyp=np.int16))`,
the result will be "steppier" than doing `LFO(offset=150,scale=100)`.
The latter uses the full 16-bit range available to `LFO`.


### Making waveforms with `ulab.numpy`

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

## Vibrato: Add LFO to pitch

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

<a href="https://www.youtube.com/watch?v=wdXAjhVb1iY" target="_blank">
<img alt="code_vibrato demo" width=640 height=360
    src="https://img.youtube.com/vi/wdXAjhVb1iY/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=wdXAjhVb1iY)


## Tremolo: Add LFO to amplitude

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

<a href="https://www.youtube.com/watch?v=3Meb5Vd8Gw8" target="_blank">
<img alt="code_tremolo demo" width=640 height=360
    src="https://img.youtube.com/vi/3Meb5Vd8Gw8/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=3Meb5Vd8Gw8)


## Fade in LFO, using LERP

If we want to "automate the automation" of turning the knob to increase and decrease
the strength of the tremolo LFO, we can use another `synthio` feature to combine two LFOs:
[`synthio.Math`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Math) and [`synthio.MathOperation`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.MathOperation).
`MathOperations` are a collection of common 3-input, 1-output tools that operate on LFOs via `Math`.
They operate at LFO update speeds in the background, so we don't have to write Python to
copy a value from an LFO, modify it, then write it to what the LFO is modifying.

One of the most useful is `MathOperation.CONSTRAINED_LERP`.  This function has three inputs:
a, b, and t.  The "a" and "b" inputs are the two signals to mix and "t" is the how much of
each you want. If t==0.0, you get just "a", if t==1.0, you get just "b", if t==0.5, you get a 50/50
mix of "a" & "b". And if you scan "t" from 0.0 to 1.0, the output of LERP looks like it's
morphing "a" into "b".  "LERP" is shorthand for "linear interpolation", which just means
making a new signal by smoothly mixing between two inputs.
A related concept is ["easing function"](https://easings.net/),
which you may be familiar with if you've done animation

In the case of fading in the tremolo effect, we can do scanning of "t" with a one-shot ramp-up LFO.
If we pass in `once=True` when making a `synthio.LFO`, the LFO only runs once, perfect for a
one-time effect. That one-time ramp LFO will be the the "t" part "mix control" of the
`MathOperation.CONSTRAINED_LERP` function, fading from "a" input of "no effect"
(i.e. amplitude is just "1.0") and the "b" input of the tremolo LFO from before.

The `CONSTRAINED_LERP` (or just "lerp") concept is so useful in `synthio` that you'll see
many times to let you choose an "amount" of something that is itself varying, like this LFO.

In the example below, `fadein_pos` is our one-time ramp controlling how much `tremolo_lfo`
to use. On each new note, `fadein_pos.retrigger()` must be called to restart that ramp.

```py
# 2_modulation/code_tremolo_fadein.py
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

fadein_pos = synthio.LFO(rate=1, once=True, waveform=np.array([0,32767], dtype=np.int16))
tremolo_lfo = synthio.LFO(rate=5, scale=0.5, offset=0.5)

fadein_tremolo_lfo = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                  1,
                                  tremolo_lfo,
                                  fadein_pos)
while True:
    midi_note = random.randint(48,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.amplitude = fadein_tremolo_lfo
    fadein_pos.retrigger()
    synth.press(note)
    for i in range(25):
        print("%.2f" % fadein_pos.value)
        time.sleep(0.05)
    synth.release(note)
    time.sleep(1)
```
> [2_modulation/code_tremolo_fadein.py](./2_modulation/code_tremolo_fadein.py)

Here's what the above code sounds like:

<a href="https://www.youtube.com/watch?v=-iMqMUAzHII" target="_blank">
<img alt="code_tremolo_fadein demo" width=640 height=360
    src="https://img.youtube.com/vi/-iMqMUAzHII/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=-iMqMUAzHII)


## Bend-in pitch envelope

Many instruments when played don't hit their target pitch immediately.
Guitar strings, for instance, start a little sharp when struck before settling
down to their pitch.  Horn players often "bend-up" into a note to hit their pitch.

We approximate that in synthesizers with an envelope on pitch.
We could use our "fade-in" LFO from our previous example,
applied directly to the `note.bend` property.

But instead let's use `synthio.MathOperation.CONSTRAINED_LERP`.
In this case, we're using the lerp to smoothly "fade" from our starting bend amount
to 0.0, no bend, i.e. our destination pitch.

Note that some of these start to sound a bit like drums.  More on that in a bit.

```py
# 2_modulation/code_lerpbend.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

while True:
    # set bend start pitch based on current note, up or down one octave
    bend_amount = random.uniform(-1, 1)
    # pick a new bend time 0.1 to 0.5
    bend_time = random.uniform(0.1, 0.5)
    # or if you want to use the knobs
    #bend_amount = -1 + knobA.value/65535 * 2
    #bend_time = (knobB.value/65535) * 0.4 + 0.1

    # this LFO automatically runs the lerp position from 0-1 over a given time
    lerp_pos = synthio.LFO(once=True, rate=1/bend_time,
                           waveform=np.array((0,32767), dtype=np.int16))
    # this MathOperation ranges from "start_val" to "end_val" over "bend_time"
    # where "start_val" is our bend_amount and "end_val" is 0 (our root pitch)
    bend_lerp = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                             bend_amount, 0.0, lerp_pos)
    note = synthio.Note(synthio.midi_to_hz(random.randint(48,60)))
    note.bend = bend_lerp   # attach our lerp to the bend

    print("bending from %.2f in %.2f seconds" % (bend_lerp.a, 1/lerp_pos.rate))
    synth.press(note)
    time.sleep(1)  # wait for bend to happen
    synth.release(note)
    time.sleep(0.1)
```
> [2_modulation/code_lerpbend.py](./2_modulation/code_lerpbend.py)

<a href="https://www.youtube.com/watch?v=4jHAdlDbcgM" target="_blank">
<img alt="code_lerpbend demo" width=640 height=360
    src="https://img.youtube.com/vi/4jHAdlDbcgM/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=4jHAdlDbcgM)


## Portamento: glide between notes

Portamento, or "glide", is the sliding of an instrument's note from one pitch to another.
This is different from pitch bend, which is usually a temporary deviation from a set pitch.

In `synthio`, we don't have an explicit portamento feature.
But we can use the lerp trick used above to glide between a "start" and "end" note.
Let's bundle up both the lerp and the glide-as-pitch-bend into a class called `Glider`.
`Glider` owns both a `MathOperation.CONSTRAINED_LERP` and a ramp-up LFO use
to automatically go between the current pitch and a new destination pitch.
The `Glider` class also knows how to calculate the difference in pitch-bend amount
to get to that new pitch.

```py
# 2_modulation/code_portamento.py
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

class Glider:
    """Attach a Glider to note.bend to implement portamento"""
    def __init__(self, glide_time, midi_note):
        self.pos = synthio.LFO(once=True, rate=1/glide_time,
                               waveform=np.array((0,32767), dtype=np.int16))
        self.lerp = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                 0, 0, self.pos)
        self.midi_note = midi_note

    def update(self, new_midi_note):
        """Update the glide destination based on new midi note"""
        self.lerp.a = self.lerp.value  # current value is now start value
        self.lerp.b = self.lerp.a + self.bend_amount(self.midi_note, new_midi_note)
        self.pos.retrigger()  # restart the lerp
        self.midi_note = new_midi_note

    def bend_amount(self, old_midi_note, new_midi_note):
        """Calculate how much note.bend has to happen between two notes"""
        return (new_midi_note - old_midi_note)  * (1/12)

    @property
    def glide_time(self):
        return 1/self.pos.rate
    @glide_time.setter
    def glide_time(self, glide_time):
        self.pos.rate = 1/glide_time

glide_time = 0.25
midi_notes = [48, 36, 24, 36]
new_midi_note = midi_notes[0]

# create a portamento glider and attach it to a note
glider = Glider(glide_time, new_midi_note)
note = synthio.Note(synthio.midi_to_hz(new_midi_note), bend=glider.lerp)
synth.press(note)   # start the note sounding

i=0
while True:
    glider.glide_time = 0.5 * (knobA.value/65535)
    new_midi_note = midi_notes[i]  # new note to glide to
    i = (i+1) % len(midi_notes)
    print("new: %d old: %d glide_time: %.2f" % (new_midi_note, glider.midi_note, glider.glide_time))
    glider.update(new_midi_note)  # glide up to new note
    time.sleep(0.5)
```

> [2_modulation/code_portamento.py](./2_modulation/code_portamento.py)

<a href="https://www.youtube.com/watch?v=v1MuPJxHKDg" target="_blank">
<img alt="code_portamento demo" width=640 height=360
    src="https://img.youtube.com/vi/v1MuPJxHKDg/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=v1MuPJxHKDg)


## Faking Exponential Amplitude Decays with LFOs

As noted at the top, `synthio.Envelope` attack and decay rates are currently linear.
And the `note.envelope` attribute can only be assigned an `Envelope`.
But we also have `synthio.Note.amplitude` that *can* be assigned a one-shot LFO,
so we can approximate an exponential release rate (or decay rate) of an ADSR
envelope by assigning an LFO to `note.amplitude` on key release.

It would look something like the example below.  Here, it's switching between
the normal linear release rate and an exponential decay release.
The difference can be subtle, but generally the exponential decay feels
"snappier" while still ringing out the same amount of time.  Try changing the
RELEASE_TIME and RELEASE_CURVE values to see how they affect the sound.

```py
# 2_modulation/code_expdecay.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth

RELEASE_TIME = 4
RELEASE_CURVE = 2.8   # 1 == linear, higher is "tighter"
env_lin = synthio.Envelope(attack_time=0, release_time=RELEASE_TIME)
env_exp = synthio.Envelope(attack_time=0, release_time=RELEASE_TIME*2)   # so it doesn't get in the way

# a waveform that's an exponential decay from 32767 to 0, shaped on RELEASE_CURVE
exp_fall_wave =  np.array(32767 * np.linspace(1, 0, num=128, endpoint=True)**RELEASE_CURVE, dtype=np.int16)
# a one-shot LFO lasting for RELEASE_TIME using the above wave
exp_fall_lfo = synthio.LFO(rate=1/RELEASE_TIME, once=True, waveform=exp_fall_wave)

i=0
while True:
    midi_note1 = 48
    if i%2==0:
        print("linear")
        note1 = synthio.Note(synthio.midi_to_hz(midi_note1), envelope=env_lin)
        synth.press(note1)
        time.sleep(0.01)
        synth.release(note1)
    else:   # every other time do linear or exponential
        print("exponential")
        note1 = synthio.Note(synthio.midi_to_hz(midi_note1), envelope=env_exp)
        synth.press(note1)
        time.sleep(0.01)
        synth.release(note1)
        exp_fall_lfo = synthio.LFO(rate=1/RELEASE_TIME, once=True, waveform=exp_fall_wave)
        note1.amplitude = exp_fall_lfo
    time.sleep(RELEASE_TIME*1.25)
    i+=1
```

> [2_modulation/code_expdecay.py](./2_modulation/code_expdecay.py)

<a href="https://www.youtube.com/watch?v=suuwS9hF0PY" target="_blank">
<img alt="code_expdecay demo" width=640 height=360
    src="https://img.youtube.com/vi/suuwS9hF0PY/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=suuwS9hF0PY)


## Fun with modulation: Drum sounds with pitch bend

Let's make a little drum synthesizer! Two things to note about drum sounds:
- the sound like sine waves as they ring
- their initial "transient" is higher-pitched that settles into their final pitch
Perfect for a pitch bend bend envelope (aka one-shot LFO) that starts high
and bends into the final pitch

Tomtom drums are pitched, so we can use lower MIDI note pitches playing sine
waves for them. Bass drums are kinda like big toms, so we'll do the same for them.
We'll talk more detail about custom oscillator waveforms in
[Oscillators and Wavetables](README-4-Oscillators-Wavetables.md).

Also in this example is a quick way of doing a snare drum. Snare drums have
little rattles on them that make a sizzling noise when they're struck. We can
approximate that with second note playing a quick random noise. Since we're
now playing two notes simultaneously, the second note will switch to non-snare
mode to add more bass to the other drum sounds.

```py
# 2_modulation/code_drum_tom.py
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

VOLUME=32767
NUM_SAMPLES=256
# drums are sine waves mostly
wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM_SAMPLES, endpoint=False)) * VOLUME, dtype=np.int16)
# snare drums have a little noise at the begining
wave_noise = np.array([random.randint(-VOLUME, VOLUME) for i in range(NUM_SAMPLES)], dtype=np.int16)
# used to make the downward pitch bend
ramp_down = np.array((32767,0), dtype=np.int16)
 # a little drum sequence: (note, time)
notes = [(40, 0.25),  # artitrary pitches that sound like high,mid,low toms
         (36, 0.25),
         (32, 0.25),
         (24, 0.5),   # 24 is lowest, so let's say it's "bass" drum
         (24, 0.5),
         (34, 0.25),  # 34 chosen arbitrarily to mean "snare"
         (24, 0.25),
         (34, 0.50)]
ni=0
while True:
    n,t = notes[ni]  # sequence step (note, time), used in release_time below
    tenv = t + ((knobA.value/65535)-0.1)  # let the knob control how drum rings out
    print("%d note:%d time:%.2f tenv:%.2f" %(ni,n,t,tenv))
    ni = (ni+1) % len(notes)  # set up next note in sequence for next time
    ramp_down_lfo = synthio.LFO(rate=1/tenv, once=True, waveform=ramp_down)
    drum_env = synthio.Envelope(attack_time=0, release_time=tenv, decay_time=0)
    drum_env2 = synthio.Envelope(attack_time=0, release_time=tenv/2, decay_time=0, attack_level=0.1,)
    note = synthio.Note(synthio.midi_to_hz(n), envelope=drum_env,
                        waveform=wave_sine,
                        bend=ramp_down_lfo,
                        )
    # second note "beefs" up the low end of the drum or adds "snare" if note==34
    note2 = synthio.Note(synthio.midi_to_hz(n/4), envelope=drum_env2,
                         waveform=wave_noise if n==34 else wave_sine)
    synth.press(note)
    synth.press(note2)
    time.sleep(0)
    synth.release(note)
    synth.release(note2)
    time.sleep(t)  # this determines our sequence speed
```
> [2_modulation/code_drum_tom.py](./2_modulation/code_drum_tom.py)

<a href="https://www.youtube.com/watch?v=8RAVexx5Oqc" target="_blank">
<img alt="code_drum_tom demo" width=640 height=360
    src="https://img.youtube.com/vi/8RAVexx5Oqc/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=8RAVexx5Oqc)



## Next steps

Now that we have some of the basics of modulation down, we can use that to
start modulating [Filters](README-3-Filters.md).
