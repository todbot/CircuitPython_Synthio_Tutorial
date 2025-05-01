# 3_filters/code_filter_envelope.py
# part of todbot circuitpython synthio tutorial
# 14 Apr 2025 - @todbot / Tod Kurt

import ulab.numpy as np
import synthio


class FilterEnvelope:
    """Simple AHR envelope for use with filters"""
    def __init__(self, max_freq, min_freq, attack_time, release_time, curve_type='linear'):
        self.max_freq = max_freq
        self.min_freq = min_freq
        self.attack_time = max(0.001, attack_time)
        self.release_time = max(0.001, release_time)
        self.lerp = synthio.LFO(once=True,
                                waveform=np.array((0,32767),dtype=np.int16))
        if curve_type == 'linear':
            lerp = self.lerp
        else:  #  'exponential'
            lerp = synthio.Math(synthio.MathOperation.PRODUCT,
                   	        self.lerp, self.lerp, 1)

        self.env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                min_freq, max_freq, lerp)

    def press(self):
        """Call this method right before synth.press()"""
        self.env.a = self.min_freq 
        self.env.b = self.max_freq
        self.lerp.rate = 1/self.attack_time
        self.lerp.retrigger()
    
    def release(self):
        """Call this method right before synth.release()"""
        self.env.a = self.env.value  # curr val is new start value
        self.env.b = self.min_freq
        self.lerp.rate = 1/self.release_time
        self.lerp.retrigger()
