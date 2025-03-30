# 5_midi/code_adafruit_midi.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import usb_midi
import adafruit_midi
from adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from synth_setup import synth

midi_usb = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], in_channel=0 )

while True:
    if msg := midi.receive():
        print("midi:",msg)
        # noteOn must have velocity > 0
        if isinstance(msg, NoteOn) and msg.velocity != 0:
            synth.press( msg.note )
        # some synths do noteOff as noteOn w/ zero velocity
        elif isinstance(msg,NoteOff) or isinstance(msg,NoteOn) and msg.velocity==0:
            synth.release( msg.note )
