
##
## Synthio Tutorial: Modulation

<!--ts-->
   * [Synthio Tutorial: Modulation](#synthio-tutorial-modulation)
      * [About LFOs](#about-lfos)
      * [Vibrato: Add LFO to pitch](#vibrato-add-lfo-to-pitch)
      * [About LFOs: offset/scale to min/max](#about-lfos-offsetscale-to-minmax)
      * [Tremolo: Add LFO to amplitude](#tremolo-add-lfo-to-amplitude)
      * [Controlling "strength" of LFO](#controlling-strength-of-lfo)
      * [Fade in LFO](#fade-in-lfo)
      * [Envelope, for amplitude](#envelope-for-amplitude)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Mon Mar 17 16:44:02 PDT 2025 -->

<!--te-->

Modulation is basically doing automated "knob-turning" of a parameter in a synthesizer.
It adds "liveliness" to a sound without you needing to be tweaking parameters by hand.

In `synthio` there are two types of modulators:

- [`Envelope`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Envelope)
   – a series of timed stages ("ADSR"), only for volume, ranges from 0.0 to 1.0, updated every sample
- [`LFO`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.LFO)
   – a (usually) repeating pattern that can affect most `synthio` parameters, by default ranges from -1.0 to 1.0, updated every 256 samples (puts a limit on fastest LFO we can have)

The `synthio` LFO modulation system is very rich, offering a set of [`MathOperations`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.MathOperation)
to let you combine an LFO with other LFOs or other parameters in your code.

### About Envelopes

The simplest modulation tool in `synthio` is the amplitude envelope, aka `synthio.Envelope`.
Unlike other sythesis systems, `Envelope` can only be used for amplitude envelope,
i.e. either `synth.envelope` (envelope for all notes) or `note.envelope` parameter (per-note envelope).
For other case where we might use an envelope,
like a pitch envelope or filter envelope, we must instead use one-shot LFOs.

In the [`synth_setup.py`](./1_getting_started/synth_setup.py) file, we set up a default
amplitude envelope that works for most of the example:

```py
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=0.6)
```
This sets the amplitude envelope for all notes played on that synth.
The amplitude envelope describes the loudness of the note over time.
It has these parameters:

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


### About LFOs

Low-frequency oscillators ("LFOs") are common in sound synthesis as a way of automating
the "knob twiddling" one might physically do to a parameter on a synthesizer.
Common uses of LFOs are for vibrato and tremolo effects.

In `synthio`, the default LFO waveform is a triangle wave that ranges from -1.0 to 1.0,
centered around zero.  You can change that range with `LFO.scale`.
And with `LFO.offset`, the waveform doesn't have to be centered around zero.
Some examples of LFOs:

```py
lfo1 = synthio.LFO(scale=0.3)  # ranges from -0.3 to +0.3
lfo2 = synthio.LFO(offset=100)  # ranges from 99 to 101
lfo2 = synthio.LFO(offset=1500, scale=500)   # ranges from 1000 to 2000
```

In the last example the LFO to ranges between 1000 and 2000, but we specify it with
offset=1500 and scale=500. That is, `offset` is the midpoint of the range and `scale` is
how much above and below that midpoint to move.

Instead of midpoint/range, we sometimes want to think of an LFO ranging from a
min/max.  To turn min/max to midpoint/range, use a function like this:

```py
def lfo_set_min_max(lfo, lmin=0.0, lmax=1.0):
    """Set an LFO's mininum and maximum values"""
    lfo.scale = (lmax - lmin)/2
    lfo.offset = lmax - lfo.scale
```

Thinking of LFOs in terms of min/max will be very helpful when dealing with filters later.


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
`scale=1/12` to only scale up and down a semitone, but I like only a single semitone of vibrato,
so `scale=0.5 * 1/12'.

Alternatively, you can have knobA control the scale and get really crazy.

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


<!-- To me, setting `offset=0.8, scale=0.2` sounds pretty good. This causes the amplitude
to range from 0.6 to 1.0.  This is a strong tremolo effect without completely shutting
off the sound. But do we have to keep adjusting `scale` & `offset` any time we want
to adjust the strength of the tremolo?  We could, but we don't have to.

Instead we can use another `synthio` feature: [`synthio.Math`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Math) and [`synthio.MathOperation`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.MathOperation).
These are a collection of common 3-input, 1-output tools that operate on LFOs and that
operate at LFO update speeds in the background, so we don't have to write Python to
copy a value from an LFO, modify it, then write it to what the LFO is modifying.
Think of it as a generalization of the `.scale` & `.offset` features of LFO.

In the tremolo case, we want a single value we can change that adjusts the "strength" of the
tremolo LFO.  The `MathOperation.PRODUCT` is good for this, we feed our LFO into one of its inputs
and a simple 0-1 number as the other input that let us turn up or down the effect.  -->


### Fade in LFO
