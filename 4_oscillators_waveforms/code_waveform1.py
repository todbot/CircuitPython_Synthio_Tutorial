# 4_oscillators/code_waveform1.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt

import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

NUM = 256    # number of samples in a waveform
VOL = 32000  # loudness of samples, np.int16 ranges from 0-32767

# sine wave, just like in trig class
wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM, endpoint=False)) * VOL, dtype=np.int16)

# sawtooth wave, looks like a downward ramp
wave_saw = np.linspace(VOL, -VOL, num=NUM, dtype=np.int16)

# square wave, like the default
wave_square = np.concatenate((np.ones(NUM // 2, dtype=np.int16) * VOL,
                              np.zeros(NUM // 2, dtype=np.int16) * -VOL))

# 'noise' wave made with random numbers (not a very good random noise)
wave_noise = np.array([random.randint(-VOL, VOL) for i in range(NUM)], dtype=np.int16)

my_waves = [wave_sine, wave_saw, wave_square, wave_noise]
my_wave_names = ["sine", "saw", "square", "noise"]

note1 = synthio.Note(0)  # start a note playing with default waveform
synth.press(note1)
wi=0  # wave index into my_waves
while True:
    note1.frequency = synthio.midi_to_hz(32 + int((knobA.value/65535)*32))
    note1.waveform = my_waves[wi]  # pick new wave for playing note
    print("wave:", wi, my_wave_names[wi])
    time.sleep( (knobB.value/65535) )  # knobB controls tempo
    wi=(wi+1) % len(my_waves)  # pick a new waveform
