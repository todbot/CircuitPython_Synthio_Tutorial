# 1_getting_started/code_midi.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import usb_midi, tmidi
from synth_setup import synth

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

while True:
    if msg := midi_usb.receive():
        print("midi:", msg)
        # noteOn must have velocity > 0
        if msg.type == tmidi.NOTE_ON and msg.velocity != 0:
            synth.press(msg.note)
        # some synths do noteOff as noteOn w/ zero velocity
        elif msg.type in (tmidi.NOTE_OFF,tmidi.NOTE_ON) and msg.velocity == 0:
            synth.release(msg.note)
