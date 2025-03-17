# 3_filters/code_filter_handmod.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
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
