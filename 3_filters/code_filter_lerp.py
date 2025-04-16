# 3_filters/code_filter_lerp.py
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth

filter_attack_time = 1.3
filter_release_time = 0.5
filter_min_freq = 200
filter_max_freq = 2000

# this LFO will automatically run the lerp position from 0 to 1 over a given timea
lerp_pos = synthio.LFO(once=True, rate=1, waveform=np.array((0,32767), dtype=np.int16))

# this MathOperation will then range from "start_val" to "end_val" over "lerp_time"
# where "start_val" is our starting frequency and "end_val" is our hold frequency)
filter_env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP, 500, 2000, lerp_pos)

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)

while True:
    midi_note = random.randint(48,72)
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                      frequency=filter_env, Q=1.8)
    # press the note
    # which means setting up the attack stage, the lerp and retriggering
    filter_env.a = filter_min_freq
    filter_env.b = filter_max_freq
    lerp_pos.rate = 1 / filter_attack_time
    lerp_pos.retrigger()
    synth.press(note)
    time.sleep(1.5)

    # release the note
    # which hmeans setting up the release stage, the lerp and retriggering
    filter_env.a = filter_max_freq
    filter_env.b = filter_min_freq
    lerp_pos.rate = 1 / filter_release_time
    lerp_pos.retrigger()
    synth.release(note)
    time.sleep(1.0)
