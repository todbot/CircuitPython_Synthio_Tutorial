# 1_getting_started/code_synth_setup.py -- Getting synthio up and running
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt

import time, random
# run all the setup and get a synth
from synth_setup import synth

midi_note = 60  # midi note to play, 60 = C4

while True:
    print("boop!")
    synth.press(midi_note) # start note playing
    time.sleep(0.1)
    synth.release(midi_note) # release the note we pressed, notice it keeps sounding
    time.sleep(0.3)
    midi_note = random.randint(32,72)   # pick a new random note

