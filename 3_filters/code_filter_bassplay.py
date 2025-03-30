import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, mixer, knobA, knobB

filter_attack_time = 1.3
filter_release_time = 0.5
filter_min_freq = 100
filter_max_freq = 4000

# this LFO will automatically run the lerp position from 0 to 1 over a given timea
lerp_pos = synthio.LFO(once=True, rate=1, waveform=np.array((0,32767), dtype=np.int16))

# this MathOperation will then range from "start_val" to "end_val" over "lerp_time"
# where "start_val" is our starting frequency and "end_val" is our hold frequency)
filter_env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP, 500, 2000, lerp_pos)

# saw wave oscillators have nicer harmonics to filter
wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)
scale_pentatonic = [0, 2, 4, 7, 9, 12]  # scale offsets
midi_note_i=0

while True:
    filter_attack_time = 0.1
    filter_release_time = 0.01 + 1.0 * (knobB.value / 65535)
    #filter_min_freq = 2000 * (knobB.value / 65535)
    filter_max_freq = 500 + 4000 * (knobA.value / 65535)
    midi_note_i = (midi_note_i+1) % len(scale_pentatonic)
    midi_note = 32 + scale_pentatonic[midi_note_i]
    #midi_note = 32 + scale_pentatonic[ int((knobB.value / 65535) * (len(scale_pentatonic)-1))]
    print("filter_attack_time:", filter_attack_time,"filter_min_freq:", filter_min_freq, "midi_note_freq:", synthio.midi_to_hz(midi_note))
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note2 = synthio.Note(synthio.midi_to_hz(midi_note*1.001), waveform=wave_saw)
    note.filter = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS,
                                      frequency=filter_env, Q=1.5)
    note2.filter = synthio.BlockBiquad(synthio.FilterMode.LOW_PASS,
                                       frequency=filter_env, Q=1.5)
    amp_env =  synthio.Envelope( attack_time = 0, 
                                 release_time = filter_release_time*1.0,)
    note.envelope = amp_env
    note2.envelope = amp_env
    # press the note
    # which means setting up the attack stage, the lerp and retriggering
    filter_env.a = filter_min_freq  # start at min
    filter_env.b = filter_max_freq  # end at max
    lerp_pos.rate = 1 / filter_attack_time
    lerp_pos.retrigger()
    synth.press(note)
    synth.press(note2)
    time.sleep(0.1)
    
    # release the note
    # which hmeans setting up the release stage, the lerp and retriggering
    filter_env.a = filter_max_freq  # start at max
    filter_env.b = filter_min_freq  # end at min
    lerp_pos.rate = 1 / filter_release_time
    lerp_pos.retrigger()
    synth.release(note)
    synth.release(note2)
    time.sleep(0.2)
