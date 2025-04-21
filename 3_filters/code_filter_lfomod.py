# 3_filters/code_filter_lfomod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
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
