# 5_midi/code_velocity.py
import usb_midi
import synthio
import tmidi
from synth_setup import synth

midi_usb = tmidi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

notes_playing = {}  # keys = midi_notes, vals = Note objs

while True:    
    if msg := midi_usb.receive():
        print("midi:", msg)
        # noteOn must have velocity > 0
        if msg.type == tmidi.NOTE_ON and msg.velocity != 0:
            velocity_normalized = msg.velocity/127
            note = synthio.Note(synthio.midi_to_hz(msg.note), 
                                envelope = synthio.Envelope(
                                    # attack level goes up with higher velocity
                                    attack_level = 0.5 + 0.5 * velocity_normalized,
                                    # sustain level goes up with higher velocity
                                    sustain_level = 0.5 + 0.4 * velocity_normalized,
                                    # attack time is faster with higher velocity
                                    attack_time = 1.0 - 0.9 * velocity_normalized,
                                    # release time is faster with higher velocity
                                    release_time = 1.5 - 1.2 * velocity_normalized,),
                                )
            synth.press(note)
            notes_playing[msg.note] = note
        elif msg.type in (tmidi.NOTE_OFF, tmidi.NOTE_ON) and msg.velocity == 0:
            if note := notes_playing.get(msg.note):
                synth.release(note)

