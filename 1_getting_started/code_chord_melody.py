# 1_getting_started/code_chord_melody.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time
from synth_setup import synth, knobA

melody_midi_notes = (50, 55, 57, 59, 59, 59, 57, 59, 55, 55)
chord = [0,4,7]
i=0
while True:
    octave = -1 + int((knobA.value/65535) * 3)  # knobA is octave offset
    midi_note = melody_midi_notes[i] + (octave*12)
    i = (i+1) % len(melody_midi_notes)
    print("playing!", midi_note)
    for n in chord: synth.press(midi_note + n)
    time.sleep(0.05)
    for n in chord: synth.release(midi_note + n)
    time.sleep(0.25)  # play around with this time for slower/faster
