# 3_filters/code_filter_keytrack.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, keys

filter_keytrack = 0.5     # filter k
filter_attack_time = 0.1   # some example values to start out with
filter_release_time = 0.4  # change them to see how it affects the sound
filter_min_freq = 100
filter_max_freq = 1000

# this LFO will run the lerp position from 0 to 1 over a given time
lerp_pos = synthio.LFO(once=True, waveform=np.array((0,32767), dtype=np.int16))
# this MathOperation ranges from "start_val" to "end_val" over "lerp_time"
filter_env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                          filter_min_freq, filter_max_freq, lerp_pos)

def set_filter_env(fstart, fend, ftime):
    filter_env.a = fstart
    filter_env.b = fend
    lerp_pos.rate = 1 / ftime
    lerp_pos.retrigger()  # must make sure to retrigger the positioner

def freq_for_keytrack(freq, midi_note, keytrack_amount):
    # generate a "scale_per_octave" that gives us 1 per octave (like CV)
    midi_base_note = 32   # below this, keytrack doesn't apply
    note_diff = max(midi_note - midi_base_note, 0)
    scale_per_octave = note_diff/12  # gives us 1 per octave
    keytrack_amount = scale_per_octave * keytrack_amount
    new_freq = freq * (1+keytrack_amount)
    #print("keytrack_amount:", keytrack_amount, new_freq, freq)
    return new_freq

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)  # osc waveform

keytrack = filter_keytrack   # start with keytracking on
while True:
    if key := keys.events.get():
        if key.pressed:   # key press switchs keytrack on/off
            keytrack = 0 if keytrack==filter_keytrack else filter_keytrack
    midi_note = 32 + int((knobA.value/65535)*32)
    new_freq = freq_for_keytrack(filter_max_freq, midi_note, keytrack)
    print("note:%d freq:%4d keytrack:%.2f keytrack_freq:%4d" %
          (midi_note, filter_max_freq, keytrack, new_freq))
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_env, Q=1.8)
    # press the note, e.g. set up the attack lerp vals and retriggering
    set_filter_env(filter_min_freq, new_freq, filter_attack_time)
    synth.press(note)
    time.sleep(filter_attack_time)

    # release the note, e.g. set up the release lerp vals and retriggering
    set_filter_env(new_freq, filter_min_freq, filter_release_time)
    synth.release(note)
    time.sleep(filter_release_time)
