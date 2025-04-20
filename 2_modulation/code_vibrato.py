# 2_modulation/code_vibrato.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
from synth_setup import synth, knobA

while True:
    midi_note = random.randint(48,72)   # pick a new random note
    note = synthio.Note(synthio.midi_to_hz(midi_note))
    bend_lfo = synthio.LFO(rate=7, scale=(1/12)*0.5)  # 7 Hz at 1 semitones warble
    note.bend = bend_lfo
    print("midi_note:",midi_note)
    #note.bend.scale = 1 * (knobA.value/65535)  # knob controls vibrato depth up to an octave
    synth.press(note) # start note playing
    time.sleep(0.5)
    synth.release(note)
    time.sleep(0.3)
