# 2_modulation/code_expdecay.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA

RELEASE_TIME = 4
RELEASE_CURVE = 2.8   # 1 == linear, higher is "tighter"
env_lin = synthio.Envelope(attack_time=0, release_time=RELEASE_TIME)
env_exp = synthio.Envelope(attack_time=0, release_time=RELEASE_TIME*2)   # so it doesn't get in the way

# a waveform that's an exponential decay from 32767 to 0, shaped on RELEASE_CURVE
exp_fall_wave =  np.array(32767 * np.linspace(1, 0, num=128, endpoint=True)**RELEASE_CURVE, dtype=np.int16)
# a one-shot LFO lasting for RELEASE_TIME using the above wave
exp_fall_lfo = synthio.LFO(rate=1/RELEASE_TIME, once=True, waveform=exp_fall_wave)

i=0
while True:
    midi_note1 = 48
    if i%2==0:
        print("linear")
        note1 = synthio.Note(synthio.midi_to_hz(midi_note1), envelope=env_lin)
        synth.press(note1)
        time.sleep(0.01)
        synth.release(note1)
    else:   # every other time do linear or exponential
        print("exponential")
        note1 = synthio.Note(synthio.midi_to_hz(midi_note1), envelope=env_exp)
        synth.press(note1)
        time.sleep(0.01)
        synth.release(note1)
        exp_fall_lfo = synthio.LFO(rate=1/RELEASE_TIME, once=True, waveform=exp_fall_wave)
        note1.amplitude = exp_fall_lfo
    time.sleep(RELEASE_TIME*1.25)
    i+=1

