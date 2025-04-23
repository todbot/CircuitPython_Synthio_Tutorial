# 4_oscillators_wavetables/code_wavewav.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA
import adafruit_wave

# reads in entire wave into RAM
# return tuple of (memoryview on the WAV, sample_rate, num_samples)
def read_waveform(filename):
    with adafruit_wave.open(filename) as w:
        if w.getsampwidth() != 2 or w.getnchannels() != 1:
            raise ValueError("unsupported format")
        return (memoryview(w.readframes(w.getnframes())).cast('h'),
                w.getframerate(), w.getnframes())

wave_wav, sample_rate, num_samples = read_waveform("/amen1_8k_s16.wav")
duration = num_samples / sample_rate
print("sample_rate:%d num_samples:%d duration:%.2f" %
      (sample_rate, num_samples, duration))

note = synthio.Note(frequency=1/duration, waveform=wave_wav) 
synth.press(note)

while True:
    note.frequency = (1/duration) * (0.25 + (knobA.value / 65535) * 1.5)
    print("note freq:%6.3f duration:%5.2f" % (note.frequency, 1/note.frequency))
    time.sleep(0.2)
