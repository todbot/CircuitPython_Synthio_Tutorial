# 1_getting_started/code_chord_melody.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time
from synth_setup import synth

melody_midi_notes = (50, 55, 57, 59, 59, 59, 57, 59, 55, 55)
chord = [0,4,7]
i=0
while True:
    midi_note = melody_midi_notes[i]
    i = (i+1) % len(melody_midi_notes)
    print("playing!", midi_note)
    for n in chord: synth.press(midi_note + n)
    time.sleep(0.1)
    for n in chord: synth.release(midi_note + n)
    time.sleep(0.1)
