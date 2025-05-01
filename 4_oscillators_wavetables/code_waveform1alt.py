# 4_oscillators/code_waveform1.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt

import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA

NUM_SAMPLES = 256
VOLUME = 32000  # np.int16 ranges from -32678 to 32767, this gives a little headroom

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM_SAMPLES, endpoint=False)) * VOLUME, dtype=np.int16)

wave_saw = np.linspace(VOLUME, -VOLUME, num=NUM_SAMPLES, dtype=np.int16)

wave_square = np.concatenate((np.ones(NUM_SAMPLES // 2, dtype=np.int16) * VOLUME,
                              np.zeros(NUM_SAMPLES // 2, dtype=np.int16) * -VOLUME))

wave_noise = np.array([random.randint(-VOLUME, VOLUME) for i in range(NUM_SAMPLES)], dtype=np.int16)

# collect waves created into a list for easy access
my_waves = [wave_sine, wave_saw, wave_square, wave_noise]

midi_note = 48
note1 = synthio.Note(synthio.midi_to_hz(midi_note))
synth.press(note1)   # start the note sounding, so we can change the waveform while it plays
time.sleep(0.5)  # let default full-scale square wave sound a bit
i=0
while True:
    i=(i+1) % len(my_waves)  # pick a new waveform
    note1.waveform = my_waves[i]  # set new waveform
    time.sleep(0.3)
