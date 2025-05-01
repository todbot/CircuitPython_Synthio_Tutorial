# 4_oscillators_waveforms/code_wavemix.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

NUM = 256    # number of samples in a waveform
VOL = 32000  # loudness (volume) of samples, np.int16 ranges from 0-32767

wave_sine = np.array(np.sin(np.linspace(0, 2*np.pi, NUM, endpoint=False)) * VOL, dtype=np.int16)
wave_saw = np.linspace(VOL, -VOL, num=NUM, dtype=np.int16)
# empty buffer we copy wave mix into
wave_empty = np.zeros(NUM, dtype=np.int16)

note = synthio.Note(frequency=220, waveform=wave_empty)
synth.press(note)

# mix between values a and b, works with numpy arrays too,  t ranges 0-1
def lerp(a, b, t):  return (1-t)*a + t*b

wave_pos = 0
while True:
  print("%.2f" % wave_pos)
  mix_speed = 0.001 + (knobA.value/65535) * 0.2  # 0.001 - 0.2
  note.waveform[:] = lerp(wave_sine, wave_saw, wave_pos)
  note.frequency = synthio.midi_to_hz(48 + (knobB.value/65535)*12)
  wave_pos = (wave_pos + mix_speed) % 1.0  # move our mix position
  time.sleep(0.01)
