# 1_getting_started/code_generative_penta.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
from synth_setup import synth

root_note = 48
scale_pentatonic = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]  # two octaves of offsets

while True:
    midi_note = root_note + random.choice(scale_pentatonic)
    print("playing!", midi_note)
    synth.press(midi_note)
    time.sleep(0.1)
    synth.release(midi_note) # release the note we pressed, notice it keeps sounding
    time.sleep(0.1)
