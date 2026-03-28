# 2_modulation/code_envelope_change.py
# part of todbot circuitpython synthio tutorial
# 28 Mar 2026 - @todbot / Tod Kurt
import time, random
import synthio
from synth_setup import synth, knobA, knobB
tempo = 3
note_duration = 2
note_on_time = 0
note_off_time =  note_duration
midi_note = 48
note = synthio.Note(synthio.midi_to_hz(midi_note))
while True:
    amp_env = synthio.Envelope(attack_time = 1 * (knobA.value/65535),
                               release_time = 1 * (knobB.value/65535))
    note.envelope = amp_env  # update the envelope
    now = time.monotonic()
    if now > note_on_time:
        note_on_time = now + tempo
        note_off_time = now + note_duration
        print("note_on: attack/release_time:", amp_env.attack_time, amp_env.release_time)
        mynote = synthio.Note(synthio.midi_to_hz(midi_note), envelope=amp_env)
        synth.press(note)
        
    if now >= note_off_time: 
        synth.release(note)

    envelope_state, env_value = synth.note_info(note)
    if envelope_state is not None and envelope_state == synthio.EnvelopeState.RELEASE:
        print("release_time:", amp_env.release_time)
        
    time.sleep(0.1)

