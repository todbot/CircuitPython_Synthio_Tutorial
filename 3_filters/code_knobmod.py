# 3_filters/code_filter_knobmod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
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
