# 3_filters/code_filter_knobmod_alt.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
# alternate version of code_filter_knobknob that uses press()/release()
import time, random, synthio
from synth_setup import synth, knobA, knobB
filter_type = synthio.FilterMode.LOW_PASS  # change to try other filters
synth.envelope=synthio.Envelope(attack_time=0, release_time=0.05,
                                attack_level=0.8)
midi_notes = (43, 48, 55, 60)
mi = 0  # which midi note to play
while True:
    note = synthio.Note(synthio.midi_to_hz(midi_notes[mi]))
    note.filter = synthio.Biquad(filter_type, frequency=800, Q=1.0)
    note.filter.frequency = (knobA.value / 65535) * 8000;  # convert to 0-8000
    note.filter.Q = (knobB.value / 65535) * 2;  # convert to 0-2
    synth.press(note)
    time.sleep(0.1)
    synth.release(note)
    print("note freq: %6.2f filter: %6.2f Q: %1.2f" %
          (note.frequency, note.filter.frequency, note.filter.Q))
    time.sleep(0.2)
    mi = (mi+1) % len(midi_notes)  # go to next midi note
