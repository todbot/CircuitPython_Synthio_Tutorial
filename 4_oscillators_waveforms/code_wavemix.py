# 4_oscillators_waveforms/code_wavemix.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA

NUM_SAMPLES = 256
VOLUME = 32000
MIX_SPEED = 0.01

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM_SAMPLES, endpoint=False)) * VOLUME, dtype=np.int16)
wave_saw = np.linspace(VOLUME, -VOLUME, num=NUM_SAMPLES, dtype=np.int16)
# empty buffer we copy wave mix into
wave_empty = np.zeros(SAMPLE_SIZE, dtype=np.int16)

note = synthio.Note(frequency=220, waveform=wave_empty)
synth.press(note)

# mix between values a and b, works with numpy arrays too,  t ranges 0-1
def lerp(a, b, t):  return (1-t)*a + t*b

wave_pos = 0
while True:
  print(wave_pos)
  note.waveform[:] = lerp(wave_sine, wave_saw, wave_pos)
  wave_pos = (wave_pos + MIX_SPEED) % 1.0  # move our mix position
  time.sleep(0.01)
