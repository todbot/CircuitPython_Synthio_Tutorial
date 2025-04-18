
# [Synthio Tutorial](.#sections): 3. Filters

<!--ts-->
   * [About Filters](#about-filters)
   * [Add a filter](#add-a-filter)
   * [Changing filter parameters with Python](#changing-filter-parameters-with-python)
   * [Changing filter with knobs](#changing-filter-with-knobs)
   * [Changing filter with LFO](#changing-filter-with-lfo)
   * [Creating filter envelope with LFOs](#creating-filter-envelope-with-lfos)
   * [Creating filter envelope with lerp LFOs](#creating-filter-envelope-with-lerp-lfos)
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
    midi_note = random.randint(48,72)
    print("playing note", midi_note)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    synth.press(note)
    # try out each filter
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=1500, Q=1.0)
    time.sleep(0.3)
    note.filter = synthio.Biquad(synthio.FilterMode.HIGH_PASS, frequency=1500, Q=1.0)
    time.sleep(0.3)
    note.filter = synthio.Biquad(synthio.FilterMode.BAND_PASS, frequency=1500, Q=1.0)
    time.sleep(0.3)
    synth.release(note)
    time.sleep(0.1)
```
> [3_filters/code_filter_tryout.py](./3_filters/code_filter_tryout.py)

```
[ ... TBD video of code_filter_tryout.py TBD ... ]
```

## Changing filter parameters with Python

The `synthio.Biquad` filter's `frequency` and `Q` parameters can be changed at
any time once the filter has been created.  This let's us do filter sweeps,
one of the hallmarks of making complex sounds.  The simplest way of adjusting
these parameters is setting them directly.

This example changes the filter frequency using Python statements,
starting at a high frequency then closing down the filter by lowering the frequency.

```py
# 3_filters/code_filter_handmod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
import time
import synthio
from synth_setup import synth
midi_note = 48
filter_types = (synthio.FilterMode.LOW_PASS,
                synthio.FilterMode.HIGH_PASS,
                synthio.FilterMode.NOTCH,
                )
i=0     # which filter we're trying
note = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note)

while True:
    print("selecting filter_type", filter_types[i])
    filter1 = synthio.Biquad(filter_types[i], frequency=3000, Q=1.2)
    note.filter = filter1

    while filter1.frequency > 250:
        print("changing filter frequency: %d" % filter1.frequency)
        filter1.frequency = filter1.frequency * 0.95  # do modulation by hand
        time.sleep(0.05)
    i = (i+1) % len(filter_types)  # go to next filter type
```
> [3_filters/code_filter_handmod.py](./3_filters/code_filter_handmod.py)

```
[ ... TBD video of code_filter_handmod.py TBD ... ]
```

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
midi_note = 60
note = synthio.Note(synthio.midi_to_hz(midi_note))
filter1 = synthio.Biquad(synthio.FilterMode.LOW_PASS, frequency=8000, Q=1.0)
note.filter = filter1
synth.press(note)

while True:
    filter1.frequency = (knobA.value / 65535) * 8000;  # convert to 0-8000
    filter1.Q = (knobB.value / 65535) * 2;  # convert to 0-2
    print("note freq: %4.2f filter freq: %4.2f Q: %1.2f" %
          (note.frequency, filter1.frequency, filter1.Q))
    time.sleep(0.05)
```
> [3_filters/code_filter_knobmod.py](./3_filters/code_filter_knobmod.py)

```
[ ... TBD video of code_filter_knobmod.py TBD ... ]
```


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
midi_note = 60
note = synthio.Note(synthio.midi_to_hz(midi_note))
# make a custom waveform, a sawtooth wave, more on this later
note.waveform = np.linspace(32000, -32000, num=128, dtype=np.int16)

filter_lfo = synthio.LFO(rate=0.75, offset=5000, scale=4500)

filter1 = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                              frequency=filter_lfo, Q=1.5)
note.filter = filter1
synth.press(note)

while True:
    print("note freq: %4.2f filter freq: %4.2f Q: %1.2f" %
          (note.frequency, filter1.frequency.value, filter1.Q))
    time.sleep(0.05)
```
> [3_filters/code_filter_lfomod.py](./3_filters/code_filter_lfomod.py)

```
[ ... TBD video of code_filter_lfomod.py TBD ... ]
```

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
from synth_setup import synth, knobA, knobB

# extend the amplitude envelope release so we can hear the filter release
synth.envelope = synthio.Envelope(attack_time=0.0, release_time=1.0)

# use a saw wave sound oscillator instead of square wave to hear the filter better
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

# parameters for our filter "envelope"
filt_attack_time = 1.0
filt_release_time = 1.5
filt_min_freq = 500
filt_max_freq = 2000

# LFO to use as the ramp up in frequency on key press
filter_attack_lfo = synthio.LFO(once=True, rate=filt_attack_time,
                                offset=filt_min_freq, scale=filt_max_freq,
                                waveform=np.array((0,32767), dtype=np.int16))
# LFO to use to ramp down the frequency on key release
filter_release_lfo = synthio.LFO(once=True, rate=filt_release_time,
                                 offset=filt_min_freq, scale=filt_max_freq,
                                 waveform=np.array((32767,0), dtype=np.int16))

while True:
    midi_note = random.randint(48,72)  # pick a new note to play
    # press a note with attack filter
    note = synthio.Note(midi_note, waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_attack_lfo, Q=1.8)
    filter_attack_lfo.retrigger()
    synth.press(note)  # trigger amp env and filter lfo

    # wait for attack phase to complete, hold a bit, then
    time.sleep(1.0)

    # release the note
    note.filter.frequency = filter_release_lfo
    filter_release_lfo.retrigger()
    synth.release(note)  # trigger amp env release

    # let the release happen
    time.sleep(1.0)

```
> [3_filters/code_filter_lfoenv.py](./3_filters/code_filter_lfoenv.py)

```
[ ... TBD video of code_filter_lfoenv.py TBD ... ]
```

## Creating filter envelope with lerp LFOs

While having two LFOs like in the previous example works, the same
trick for a bend-in pitch envelope using `MathOperation.CONSTRAINED_LERP` can
be used to make an AHR filter envelope.

The benefit of this technique is the same object is used for `note.frequency.filter`,
no reassignment needed.

```py
# 3_filters/code_filter_lerp.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth

filter_attack_time = 1.3
filter_release_time = 0.5
filter_min_freq = 200
filter_max_freq = 2000

# this LFO will automatically run the lerp position from 0 to 1 over a given timea
lerp_pos = synthio.LFO(once=True, rate=1, waveform=np.array((0,32767), dtype=np.int16))

# this MathOperation will then range from "start_val" to "end_val" over "lerp_time"
# where "start_val" is our starting frequency and "end_val" is our hold frequency)
filter_env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP, 500, 2000, lerp_pos)

# saw wave oscillators have nicer harmonics to filter
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

while True:
    midi_note = random.randint(32,60)
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                      frequency=filter_env, Q=2.0)
    # press the note
    # which means setting up the attack stage, the lerp and retriggering
    filter_env.a = filter_min_freq  # start at min
    filter_env.b = filter_max_freq  # end at max
    lerp_pos.rate = 1 / filter_attack_time
    lerp_pos.retrigger()
    synth.press(note)
    time.sleep(1.5)

    # release the note
    # which hmeans setting up the release stage, the lerp and retriggering
    filter_env.a = filter_max_freq  # start at max
    filter_env.b = filter_min_freq  # end at min
    lerp_pos.rate = 1 / filter_release_time
    lerp_pos.retrigger()
    synth.release(note)
    time.sleep(1.0)
```

```
[ ... TBD video of code_filter_lerp.py TBD ... ]
```

## Next steps

Filters are a key way to sculpt a sound, but in `synthio` we have an even 
more powerful technique for sound sculpting: 
[Oscillators and Wavetables](README-4-Oscillators-Wavetables.md).
