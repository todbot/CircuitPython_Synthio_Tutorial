# 2_modulation/code_vibrato.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
from synth_setup import synth

bend_lfo = synthio.LFO(rate=7, scale=0.05)  # 7 Hz at 5%

while True:
    print("boop!",midi_note)
    midi_note = random.randint(48,72)   # pick a new random note
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    note.bend = bend_lfo
    synth.press(note) # start note playing
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.3)
