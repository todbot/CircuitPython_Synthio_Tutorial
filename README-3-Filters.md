#
# Synthio Tutorial: Filters

<!--ts-->
   * [Synthio Tutorial: Filters](#synthio-tutorial-filters)
      * [Add a filter](#add-a-filter)
      * [Changing filter parameters by hand](#changing-filter-parameters-by-hand)
      * [Add LFO to a filter](#add-lfo-to-a-filter)

<!-- Created by https://github.com/ekalinin/github-markdown-toc -->
<!-- Added by: tod, at: Wed Mar 12 09:28:31 PDT 2025 -->

<!--te-->

something something about filters

## Add a filter


## Changing filter parameters by hand

This example automatically changes the filter, starting high then closing down the filter.

```py
# 3_filters/code_filter_automod.py
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
# 3_filters/code_filter_knobs.py
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

Instead of twiddling the knobs by hand, we can use LFOs to help us here.and we have LFOs to help us here.



## With Envelope on press

A common synthesis technique is to have an envelope on the filter frequency.
The Envelopes in `synthio` cannot be plugged directly into `BlockBiquad`.
