#
# Synthio Tutorial: Filters

<!--ts-->
* [Synthio Tutorial: Filters](#synthio-tutorial-filters)
   * [Add a filter](#add-a-filter)
   * [Changing filter parameters by hand](#changing-filter-parameters-by-hand)
   * [Add LFO to a filter](#add-lfo-to-a-filter)
   * [With Envelope on press](#with-envelope-on-press)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Mon Mar 17 16:43:53 PDT 2025 -->

<!--te-->

something something about filters

## Add a filter


## Changing filter parameters by hand

This example automatically changes the filter, starting high then closing down the filter.

```py
# 3_filters/code_filter_handmod.py
import synthio
from synth_setup import synth
midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note)

while True:
    print("changing filter frequency")
    filter1.frequency = filter1.frequency * 0.95  # do modulation by hand
    if filter1.frequency < 250:
        filter1.frequency = 3000
    time.sleep(0.01)
```

And here's a similar idea but with using the knobs to adjust filter cutoff and resonance.

Note the filter becomes glitchy and unstable when its frequency approaches the
note frequency, especially at high resonsance ("Q") values.  This is a feature of how
the filter is currently implemented in `synthio` and the work-around is to make sure your
filter frequency stays above 1.5x the note frequency.

```py
# 3_filters/code_filter_knobmod.py
import time, synthio
from synth_setup import synth, knobA, knobB
midi_note = 60
note = synthio.Note(synthio.midi_to_hz(midi_note))
filter1 = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS, frequency=8000, Q=1.0)
note.filter = filter1
synth.press(note)

while True:
    filter1.frequency = (knobA.value / 65535) * 8000;  # convert to 0-8000
    filter1.Q = (knobB.value / 65535) * 2;  # convert to 0-2
    print("note freq: %4.2f filter freq: %4.2f Q: %1.2f" %
          (note.frequency, filter1.frequency, filter1.Q))
    time.sleep(0.05)
```

## Add LFO to a filter

Instead of twiddling the knobs by hand, we can use LFOs!

The default LFO waveform is a triangle wave that goes from -1 to +1, starting
at zero and going up.  Using `LFO.scale` & `LFO.offset`, we can turn that -1->+1
range into any range we want with a bit of math. 

For instance, if we want the LFO to range between 500 and 1500, we could create
it like this: `lfo = synthio.LFO(rate=0.5, offset=1000, scale=500)`. 
That is, `offset` is the midpoint of the range you want and `scale` is 
how much above and below that midpoint to move. 

Instead of midpoint/range, we sometimes want to think of an LFO ranging from a
min/max.  To turn min/max to midpoint/range, use a function like this:
```py
 def set_min_max(lfo, lmin=0.0, lmax=1.0):
   lfo.scale = (lmax - lmin)
   lfo.offset = lmax - lfo.scale
```

We can create an LFO like this: 
```py
min_freq = 500
max_freq = 5500
lfo1 = syhnthio.LFO(rate=0.5, offset=, scale=...
```


```py
# 3_filters/code_lfomod.py
import time, synthio
import ulab.numpy as np
from synth_setup import synth, knobA, knobB
midi_note = 60
note = synthio.Note(synthio.midi_to_hz(midi_note))
# make a custom waveform, a sawtooth wave, more on this later
note.waveform = np.linspace(32000, -32000, num=128, dtype=np.int16)

filter_lfo = synthio.LFO(rate=0.75, offset=5000, scale=4500)

filter1 = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS, 
                              frequency=filter_lfo, Q=1.5)
note.filter = filter1
synth.press(note)

while True:
    print("note freq: %4.2f filter freq: %4.2f Q: %1.2f" %
          (note.frequency, filter1.frequency.value, filter1.Q))
    time.sleep(0.05)
```

## With Envelope on press

A common synthesis technique is to put an envelope on the filter frequency, 
much as you'd do this for the oscillator amplitude.  Many synths have two dedicated
envelopes: one on amplitude and one on filter cutoff. 
In `synthio`, the Envelopes cannot be plugged directly into anything other than
`synthio.amplitude` or `note.amplitude`. 

Instead, we must create an approximation of an envelope using multiple one-time LFOs.
The most important segements of an envelope are the attack and the release.
This makes it easier for us: we can assign a ramp-up LFO when a note is pressed 
and a ramp-down LFO when the note is released.

```py
# 3_filters/code_lfomod.py
import time, random, synthio
import ulab.numpy as np
from synth_setup import synth, knobA, knobB

synth.envelope = synthio.Envelope(attack_time=0.0, release_time=1.5)

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

min_freq = 500
max_freq = 2000

filter_attack_lfo = synthio.LFO(once=True, rate=1.0, offset=min_freq, scale=max_freq,
                                waveform=np.array((0,32767), dtype=np.int16))
                                
filter_release_lfo = synthio.LFO(once=True, rate=1.5, offset=min_freq, scale=max_freq,
                                 waveform=np.array((32767,0), dtype=np.int16))
                                 
midi_note = 60
while True:
    # press a note with attack filter
    note = synthio.Note(midi_note, waveform=wave_saw)
    note.filter = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS, 
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

    midi_note = random.randint(48,72)  # pick a new note to play
```

