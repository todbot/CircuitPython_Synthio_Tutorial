# 2_modulation/code_drum_tom.py
import time, random
import synthio
import ulab.numpy as np
from synth_setup import synth, knobA

VOLUME=32767
NUM_SAMPLES=256
# drums are sine waves mostly
wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM_SAMPLES, endpoint=False)) * VOLUME, dtype=np.int16)
# snare drums have a little noise at the begining
wave_noise = np.array([random.randint(-VOLUME, VOLUME) for i in range(NUM_SAMPLES)], dtype=np.int16)
# used to make the downward pitch bend
ramp_down = np.array((32767,0), dtype=np.int16)
 # a little drum sequence: (note, time)
notes = [(40, 0.25),  # artitrary pitches that sound like high,mid,low toms
         (36, 0.25),
         (32, 0.25),
         (24, 0.5),   # 24 is lowest, so let's say it's "bass" drum
         (24, 0.5),  
         (34, 0.25),  # 34 chosen arbitrarily to mean "snare"
         (24, 0.25),
         (34, 0.50)]
ni=0
while True:
    n,t = notes[ni]  # sequence step (note, time), used in release_time below
    tenv = t + ((knobA.value/65535)-0.1)
    ni = (ni+1) % len(notes)  # set up next note in sequence for next time
    print("note:%d time:%.2f" %(n,t))
    ramp_down_lfo = synthio.LFO(rate=1/tenv, once=True, waveform=ramp_down) 
    drum_env = synthio.Envelope(attack_time=0, release_time=tenv, decay_time=0)
    drum_env2 = synthio.Envelope(attack_time=0, release_time=tenv/2, decay_time=0, attack_level=0.1,)
    note = synthio.Note(synthio.midi_to_hz(n),
                        waveform=wave_sine,
                        envelope=drum_env,
                        bend=ramp_down_lfo,
                        )
    # second note "beefs" up the low end of the drum or adds "snare" if note==34
    note2 = synthio.Note(synthio.midi_to_hz(n/4),
                         waveform=wave_noise if n==34 else wave_sine,
                         envelope=drum_env2)
    synth.press(note)
    synth.press(note2)
    time.sleep(0)
    synth.release(note)
    synth.release(note2)
    time.sleep(t)  # this determines our sequence speed
