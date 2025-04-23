# 3_filters/code_filter_keytrack.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, keys

from filter_envelope import FilterEnvelope

filter_keytrack = 0.5  # filter keytracking,0=none, 1=full track
filter_max_freq = 1000
filter_min_freq = 100

def keytrack_filter_env(filter_env, midi_note, keytrack_amount):
    """ adjust a FilterEnvelope max_freq based on keytrack_amount"""
    # generate a "scale_per_octave" that gives us 1 per octave (like CV)
    midi_base_note = 32   # below this, keytrack doesn't apply
    note_diff = max(midi_note - midi_base_note, 0)
    scale_per_octave = note_diff/12  # gives us 1 per octave
    keytrack_amount = scale_per_octave * keytrack_amount
    filter_env.max_freq = filter_env.max_freq * (1+keytrack_amount)

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)  # saw osc

keytrack = filter_keytrack   # start with keytracking on
while True:
    if key := keys.events.get():
        if key.pressed:   # key press switchs keytrack on/off
            keytrack = 0 if keytrack==filter_keytrack else filter_keytrack
    midi_note = 32 + int((knobA.value/65535)*32)
    
    filter_env = FilterEnvelope(filter_max_freq, filter_min_freq, 0, 0.4)
    
    keytrack_filter_env(filter_env, midi_note, keytrack)
    
    filter =  synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_env.env, Q=1.8)
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw,
                        filter=filter)
    print("note:%d forig:%4d track:%.2f fnew:%4d" %
          (midi_note, filter_max_freq, keytrack, filter_env.max_freq))

    filter_env.press()
    synth.press(note)
    time.sleep(0.1)

    filter_env.release()
    synth.release(note)
    time.sleep(filter_env.release_time)

