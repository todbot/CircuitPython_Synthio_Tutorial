# 3_filters/code_filter_envclass.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt
#
import time, random
import ulab.numpy as np
import synthio
from synth_setup import synth, knobA, knobB

class FilterEnvelope:
    def __init__(self, max_freq, min_freq, attack_time, release_time):
        self.max_freq, self.min_freq = max_freq, min_freq
        self.attack_time, self.release_time = attack_time, release_time
        self.lerp = synthio.LFO(once=True,
                                waveform=np.array((0,32767), dtype=np.int16))
        self.env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                min_freq, max_freq, self.lerp)
    def press(self):
        self.env.a = self.min_freq
        self.env.b = self.max_freq
        self.lerp.rate = 1/self.attack_time
        self.lerp.retrigger()
        
    def release(self):
        self.env.a = self.env.value  # curr val is new start value
        self.env.b = self.min_freq
        self.lerp.rate = 1/self.release_time
        self.lerp.retrigger()

wave_saw = np.linspace(32000, -32000, num=128, dtype=np.int16)  # saw osc
while True:
    midi_note = random.randint(24,52)
    attack_time  = 0.005 + 1.0*(knobA.value/65535)
    release_time = 0.005 + 1.0*(knobB.value/65535)
    filter_env = FilterEnvelope(3000, 200, attack_time, release_time)
    amp_env = synthio.Envelope(attack_time=0, release_time=release_time*1.5)
    print("note: %d fenv attack:%.3f release:%.3f" %
          (midi_note, attack_time, release_time))
    note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wave_saw)
    note.envelope = amp_env
    note.filter = synthio.Biquad(synthio.FilterMode.LOW_PASS,
                                 frequency=filter_env.env, Q=1.4)
    filter_env.press()
    synth.press(note)
    time.sleep(attack_time*2)

    filter_env.release()
    synth.release(note)
    time.sleep(release_time)
