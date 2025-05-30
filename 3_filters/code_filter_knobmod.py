# 3_filters/code_filter_knobmod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
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
