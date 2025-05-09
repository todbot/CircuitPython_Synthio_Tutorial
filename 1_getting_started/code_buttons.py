# 1_getting_started/code_buttons.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#

from synth_setup import synth, keys

root_note = 48  # the lowest note to play

while True:
    if key := keys.events.get():
        midi_note = root_note + key.key_number  # different note for each key
        if key.pressed:
            print("press!")
            synth.press(midi_note)
        if key.released:
            print("release!")
            synth.release(midi_note)
