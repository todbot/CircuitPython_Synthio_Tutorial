# code_play_big_wav_badly.py  -- play a larger WAV as a synthio.Note, badly
# 
import time
import synthio
import ulab.numpy as np
from synth_setup import mixer, synth, knobA, knobB, keys
from wavetable import Wavetable

wt1 = Wavetable("/amen1_22k_s16.wav", wave_len=512)
duration = wt1.num_samples / wt1.sample_rate
print("duration:", duration, "num_waves:",wt1.num_waves, "samples:",wt1.num_samples, wt1.sample_rate)

note = synthio.Note(frequency = wt1.sample_rate / wt1.wave_len,
                    waveform = wt1.waveform,
                    envelope = synthio.Envelope(attack_time=0, attack_level=1, sustain_level=1))
synth.press(note)

wav_pos = synthio.LFO(rate=1/duration, scale=wt1.num_waves-1, interpolate=False,
                      waveform=np.linspace(0, 32767, num=wt1.num_waves, dtype=np.int16))
synth.blocks.append(wav_pos)  #  start lfo running

while True:
    wt1.wave_pos = wav_pos.value
    time.sleep(1/wt1.sample_rate)
