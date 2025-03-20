# 3_filters/code_filter_tryout.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
from synth_setup import synth

while True:
    midi_note = random.randint(48,72)
    print("playing note", midi_note)
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    synth.press(note)
    # try out each filter
    note.filter = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS, frequency=1000, Q=1.0)
    time.sleep(0.5)
    note.filter = synthio.BlockBiquad(synthio.FilterMode.HIGH_PASS, frequency=1000, Q=1.0)
    time.sleep(0.5)
    note.filter = synthio.BlockBiquad(synthio.FilterMode.BAND_PASS, frequency=1000, Q=1.0)
    time.sleep(0.5)    
    synth.release(note)
    time.sleep(0.1)
