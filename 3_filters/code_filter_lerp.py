# 3_filters/code_filter_lerp.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA

filter_attack_time = 0.1   # some example values to start out with
filter_release_time = 0.6  # change them to see how it affects the sound
filter_min_freq = 100
filter_max_freq = 4000

# this LFO will automatically run the lerp position from 0 to 1 over a given timea
lerp_pos = synthio.LFO(once=True, waveform=np.array((0,32767), dtype=np.int16))

# this MathOperation will range from "start_val" to "end_val" over "lerp_time"
# where "start_val" is our starting frequency and "end_val" is our hold frequency)
filter_env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                          filter_min_freq, filter_max_freq, lerp_pos)

def set_filter_lerp(fstart, fend, ftime):
    filter_env.a = fstart
    filter_env.b = fend
    lerp_pos.rate = 1 / ftime
    lerp_pos.retrigger()  # must make sure to retrigger the positioner
    
# nice little saw wave oscillator sounds better than default sqaure
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

while True:
    midi_note = 32 + int((knobA.value/65535)*32)  #random.randint(48,60)
    print("playing note:", midi_note)
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_env, Q=1.8)
    # press the note, e.g. set up the attack lerp vals and retriggering 
    set_filter_lerp(filter_min_freq, filter_max_freq, filter_attack_time)
    synth.press(note)
    time.sleep(filter_attack_time)

    # release the note, e.g. set up the release lerp vals and retriggering
    set_filter_lerp(filter_max_freq, filter_min_freq, filter_release_time)
    synth.release(note)
    time.sleep(filter_release_time)
