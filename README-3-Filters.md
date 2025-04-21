
# [Synthio Tutorial](.#sections): 3. Filters

<!--ts-->
   * [About Filters](#about-filters)
   * [Add a filter](#add-a-filter)
   * [Changing filter parameters with Python](#changing-filter-parameters-with-python)
   * [Changing filter with knobs](#changing-filter-with-knobs)
   * [Changing filter with LFO](#changing-filter-with-lfo)
   * [Creating filter envelope with LFOs](#creating-filter-envelope-with-lfos)
   * [Creating filter envelope with lerp LFOs](#creating-filter-envelope-with-lerp-lfos)
   * [Fun with filters: sample &amp; hold filter envelope](#fun-with-filters-sample--hold-filter-envelope)
   * [Next steps](#next-steps)
<!--te-->

## About Filters

Perhaps the most recognizable sound in synthesizers is the **bwwooooowwwww* of a
high-resonance low-pass filter sweep moving across the frequency range.
There are many different filter types in synthesis and digital recreation of those filters.
But filter emulation is tricky and computationally expensive,
so you'll see many microcontroller synthesis platforms with little or no filters available.

In `synthio`, there is an efficient two-pole filter design with adjustable
frequency and resonance based on the [Biquad Filter Formula](https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html)
called [`synthio.Biquad`](https://docs.circuitpython.org/en/latest/shared-bindings/synthio/index.html#synthio.Biquad_).

Biquad provides the standard filter types:

- low-pass
- high-pass
- band-pass
- notch
- high-/low-shelf
- peaking

(Note: `Biquad` used to be `BlockBiquad` because its inputs could be modulated
with LFOs, which are of type `BlockInput`. As of CircuitPython 10, it's just called `Biquad`)

Only one filter can be attached to a `synthio.Note`, filters cannot be stacked. However,
if your platform supports the [`audiofilters` module](https://docs.circuitpython.org/en/latest/shared-bindings/audiofilters/index.html) then you have
access to [`audiofilters.Filter`](), which can be stacked.

## Add a filter

The `synthio.Note` object has a `.filter` property that can be assigned with a `Biquad` object.
This `.filter` property can be re-assigned to change the filter type while the Note is sounding.
This means that *each Note can have its own filter* with its own filter properties!

This example creates a `synthio.Note` object, creating and assigning one of three different
filter types in turn.  The frequency and resonance of the filters are fixed for now.

```py
# 3_filters/code_filter_tryout.py
import time, random
import synthio
from synth_setup import synth

while True:
    midi_note = random.randint(36,60)
    print("playing note", midi_note)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    synth.press(note)
    # try out each filter by assigning to note.filter
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=1000, Q=1.0)
    time.sleep(0.5)
    note.filter = synthio.Biquad(synthio.FilterMode.HIGH_PASS, frequency=1000, Q=1.0)
    time.sleep(0.5)
    note.filter = synthio.Biquad(synthio.FilterMode.BAND_PASS, frequency=1000, Q=1.0)
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.2)
```
> [3_filters/code_filter_tryout.py](./3_filters/code_filter_tryout.py)

<a href="https://www.youtube.com/watch?v=oo35ITF87BY" target="_blank">
<img alt="code_filter_tryout demo" width=640 height=360
    src="https://img.youtube.com/vi/oo35ITF87BY/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=oo35ITF87BY)


## Changing filter parameters with Python

The `synthio.Biquad` filter's `frequency` and `Q` parameters can be changed at
any time once the filter has been created.  This let's us do filter sweeps,
one of the hallmarks of making complex sounds.  The simplest way of adjusting
these parameters is setting them directly.

This example changes the filter frequency using Python statements,
starting at a high frequency then closing down the filter by lowering the frequency.

```py
# 3_filters/code_filter_handmod.py
import time
import synthio
from synth_setup import synth
midi_note = 48  # C2
filter_types = (synthio.FilterMode.LOW_PASS,
                synthio.FilterMode.HIGH_PASS,
                synthio.FilterMode.BAND_PASS,
                synthio.FilterMode.NOTCH)
i=0     # which filter we're trying
note = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note)

while True:
    print("selecting filter_type:\n  ", filter_types[i])
    filter1 = synthio.Biquad(filter_types[i], frequency=4000, Q=1.2)
    note.filter = filter1  # set the filter for this note

    while filter1.frequency > 250:
        print("filter frequency: %d" % filter1.frequency)
        filter1.frequency = filter1.frequency * 0.95  # do modulation by hand
        time.sleep(0.03)
    i = (i+1) % len(filter_types)  # go to next filter type
```
> [3_filters/code_filter_handmod.py](./3_filters/code_filter_handmod.py)

<a href="https://www.youtube.com/watch?v=ggCszD6noBo" target="_blank">
<img alt="code_filter_handmod demo" width=640 height=360
    src="https://img.youtube.com/vi/ggCszD6noBo/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=ggCszD6noBo)

## Changing filter with knobs

Here's a similar idea but with using the knobs to adjust filter cutoff and resonance.
It's a fun way to find good combinations of those parameters.

Note the filter becomes glitchy and unstable when its frequency approaches the
note frequency, especially at high resonsance ("Q") values.  This is a feature of how
the filter is currently implemented in `synthio` and the work-around is to make sure your
filter frequency stays about 1.5x above the note frequency.

```py
# 3_filters/code_filter_knobmod.py
import time, synthio
from synth_setup import synth, knobA, knobB
midi_notes = (43, 48, 55, 60)
mi=0
note = synthio.Note(synthio.midi_to_hz(midi_notes[mi]))
filter1 = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=8000, Q=1.0)
note.filter = filter1
synth.press(note)

while True:
    for _ in range(20):
        filter1.frequency = (knobA.value / 65535) * 8000;  # 0-8000
        filter1.Q = (knobB.value / 65535) * 2;  # convert to 0-2
        print("note freq: %6.2f filter freq: %4d Q: %1.2f" %
              (note.frequency, filter1.frequency, filter1.Q))
        time.sleep(0.05)
    mi = (mi+1) % len(midi_notes)  # go to next note
    note.frequency = synthio.midi_to_hz(midi_notes[mi])
```
> [3_filters/code_filter_knobmod.py](./3_filters/code_filter_knobmod.py)

<a href="https://www.youtube.com/watch?v=RSFnHbDJWf4" target="_blank">
<img alt="code_filter_knobmod demo" width=640 height=360
    src="https://img.youtube.com/vi/RSFnHbDJWf4/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=RSFnHbDJWf4)


## Changing filter with LFO

While changing a filter directly in Python works, it's less efficient and not as smooth
sounding as using an LFO, since an LFO works in the background, not requiring any
code on our part.

This example raises and lowers the filter frequency using an LFO.
This example also swaps out the default square wave waveform Note oscillator
for a simple saw wave, which has more musical harmonics that are easier to hear
being filtered out.

```py
# 3_filters/code_filter_lfomod.py
import time, synthio
import ulab.numpy as np
from synth_setup import synth, knobA, knobB
midi_notes = (43, 48, 55, 60)   # a little arpeggio
mi = 0  # which midi note to play
note = synthio.Note(synthio.midi_to_hz(midi_notes[mi]))
# make a custom sawtooth waveform, more on this later
note.waveform = np.linspace(32000, -32000, num=128, dtype=np.int16)
# lfo to turn the filter frequency "knob" for us
filter_lfo = synthio.LFO(rate=0.75, offset=4000, scale=3700)
filter1 = synthio.Biquad(synthio.FilterMode.BAND_PASS,
                         frequency=filter_lfo, Q=1.5)
note.filter = filter1
synth.press(note)

while True:
    for _ in range(20):
        print("note freq: %6.2f filter freq: %4d Q: %1.2f" %
              (note.frequency, filter1.frequency.value, filter1.Q))
        filter_lfo.rate = (knobA.value/65535) * 20  # 0-20
        filter1.Q = (knobB.value/65535) * 2  # 0-2
        time.sleep(0.05)
    mi = (mi+1) % len(midi_notes)  # go to next note
    note.frequency = synthio.midi_to_hz(midi_notes[mi])
```
> [3_filters/code_filter_lfomod.py](./3_filters/code_filter_lfomod.py)

<a href="https://www.youtube.com/watch?v=Ez8TSuOGduc" target="_blank">
<img alt="code_filter_lfomod demo" width=640 height=360
    src="https://img.youtube.com/vi/Ez8TSuOGduc/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=Ez8TSuOGduc)

## Creating filter envelope with LFOs

A common synthesis technique is a ADSR filter envelope on the filter frequency,
triggered similar to an amplitude envelope. Many synths have two dedicated
envelopes: one on amplitude and one on filter cutoff.
Remember in `synthio`, `Envelopes` cannot be plugged directly into anything other than
`synthio.amplitude` or `note.amplitude`.

Instead, we must create an approximation of an ADSR envelope using multiple one-shot LFOs.
The most important parts of an envelope are the attack and the release phases.
This makes it easier for us: we assign a ramp-up LFO when the note is pressed
and a ramp-down LFO when the note is released.
This is called an AHR (attack-hold-release) envelope.

```py
# 3_filters/code_filter_lfoenv.py
import time, random, synthio
import ulab.numpy as np
from synth_setup import synth
# extend the amplitude envelope release so we can hear the filter release
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=1.2)
# use a saw wave oscillator instead of square wave to hear the filter better
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)
# parameters for our filter "envelope"
filt_attack_time = 1.5
filt_release_time = 0.75
filt_min_freq = 100
filt_max_freq = 2000

# LFO to use as the ramp up in frequency on key press
filter_attack_lfo = synthio.LFO(once=True, rate=1/filt_attack_time,
                                offset=filt_min_freq, scale=filt_max_freq,
                                waveform=np.array((0,32767), dtype=np.int16))
# LFO to use to ramp down the frequency on key release
filter_release_lfo = synthio.LFO(once=True, rate=1/filt_release_time,
                                 offset=filt_min_freq, scale=filt_max_freq,
                                 waveform=np.array((32767,0), dtype=np.int16))
while True:
    midi_note = random.randint(48,72)  # pick a new note to play
    print("filter up!")
    # press a note with attack filter
    note = synthio.Note(midi_note, waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_attack_lfo, Q=1.8)
    filter_attack_lfo.retrigger()
    synth.press(note)  # trigger amp env and filter lfo

    time.sleep(filt_attack_time)  # wait for note attack to finish, then

    note.filter.frequency = filter_release_lfo   # release the note
    filter_release_lfo.retrigger()
    synth.release(note)  # trigger amp env release
    print("filter down!")

    time.sleep(filt_release_time)   # let the release happen
```
> [3_filters/code_filter_lfoenv.py](./3_filters/code_filter_lfoenv.py)

<a href="https://www.youtube.com/watch?v=KoIuInQ0yR8" target="_blank">
<img alt="code_filter_lfoenv demo" width=640 height=360
    src="https://img.youtube.com/vi/KoIuInQ0yR8/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=KoIuInQ0yR8)

## Creating filter envelope with lerp LFOs

While having two LFOs like in the previous example works, the same
trick for a bend-in pitch envelope using `MathOperation.CONSTRAINED_LERP` can
be used to make an AHR filter envelope.

The benefit of this technique is the same object is used for `note.frequency.filter`,
no reassignment needed. So it's more efficient (for CircuitPython)
and easier to think about (for us).

Finally we have a pretty usable AHR-like filter envelope in `synthio`.
All it took was a one-shot `synthio.LFO` controlling a `synthio.MathOperation`
CONSTRAINED_LERP that we retrigger on both `synth.press()` and `synth.release()`!
Yes, okay, actually this is a lot of components we have to hook together, but
the semi-modular nature of `synthio` means we have a lot of power to hook things
up differently to create other kinds of sounds.

In the example below, the four main parameters of the filter envelope are brought
out as variables. Try changing them to see how it affects the sound. The main
`while`-loop triggers notes chosen by knobA and makes sure to sleep long enough
between `synth.press()` and `synth.release()` so you can hear the filter attack.
In the demo video, you can see me editing some of these values and reloading.

It's starting to sound like a real synth!

```py
# 3_filters/code_filter_lerp.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA

filter_attack_time = 0.1   # some example values to start out with
filter_release_time = 0.6  # change them to see how it affects the sound
filter_min_freq = 100
filter_max_freq = 2000

# this LFO will automatically run the lerp position from 0 to 1 over a given time
lerp_pos = synthio.LFO(once=True, waveform=np.array((0,32767), dtype=np.int16))

# this MathOperation will range from "start_val" to "end_val" over "lerp_time"
# where "start_val" is our starting frequency and "end_val" is our hold frequency)
filter_env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                          filter_min_freq, filter_max_freq, lerp_pos)

def set_filter_env(fstart, fend, ftime):
    filter_env.a = fstart
    filter_env.b = fend
    lerp_pos.rate = 1 / ftime
    lerp_pos.retrigger()  # must make sure to retrigger the positioner

# nice little saw wave oscillator sounds better than default square
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

while True:
    midi_note = 32 + int((knobA.value/65535)*32)  #random.randint(48,60)
    print("playing note:", midi_note)
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_env, Q=1.8)
    # press the note, e.g. set up the attack lerp vals and retriggering
    set_filter_env(filter_min_freq, filter_max_freq, filter_attack_time)
    synth.press(note)
    time.sleep(filter_attack_time)

    # release the note, e.g. set up the release lerp vals and retriggering
    set_filter_env(filter_max_freq, filter_min_freq, filter_release_time)
    synth.release(note)
    time.sleep(filter_release_time)
```
> [3_filters/code_filter_lfoenv.py](./3_filters/code_filter_lerp.py)

<a href="https://www.youtube.com/watch?v=VubIJVZqy8E" target="_blank">
<img alt="code_filter_lerp demo" width=640 height=360
    src="https://img.youtube.com/vi/VubIJVZqy8E/maxresdefault.jpg"></a>

[youtube video](https://www.youtube.com/watch?v=VubIJVZqy8E )


## Fun with filters: sample & hold filter envelope

When used with a low-pass filter, the sample-and-hold effect works best
when you can really close down the filter (set the filter frequency to zero).
Because of the glitches the synthio low-pass filter has, this example uses
the band-pass filter, which has fewer glitches and lets us crank the resonance!

```py
# 3_filters/code_filter_sandh.py
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

# make a quicky saw wave for oscillator
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

# and a "random" wave for sample-n-hold effect
wave_rand = np.array([random.randint(-32000, 32000) for i in range(128)], dtype=np.int16)
lfo_sh = synthio.LFO(rate=0.05, interpolate=False, waveform=wave_rand, offset=300, scale=200)
filt = synthio.Biquad(synthio.FilterMode.BAND_PASS, frequency=lfo_sh, Q=2.8)

midi_note = 36
note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw, filter=filt)
synth.press(note)

while True:
    print("%d" % lfo_sh.value)
    time.sleep(0.05)
    vA = knobA.value/65535
    vB = knobB.value/65535
    lfo_sh.offset = 100 + vA*1000
    lfo_sh.scale = lfo_sh.offset * .75
```

> [3_filters/code_filter_sandh.py](./3_filters/code_filter_sandh.py)

```
[ ... TBD video of code_filter_sandh.py TBD ... ]
```


## Next steps

Filters are a key way to sculpt a sound, and we can do a lot now.
But in `synthio` we have an even more powerful technique for sound sculpting:
[Oscillators and Wavetables](README-4-Oscillators-Wavetables.md).
