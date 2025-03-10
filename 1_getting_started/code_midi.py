# 1_getting_started/code_midi.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import synthio
import usb_midi, tmidi
from synth_setup import synth, keys

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

while True:
    if msg := midi_usb.receive():
        print("midi:", msg)
        if msg.type == tmidi.NOTE_ON and msg.velocity > 0:
            synth.press(msg.note)
        elif msg.type == tmidi.NOTE_OFF or msg.velocity == 0:
            synth.release(msg.note)
