
import ulab.numpy as np
import synthio

LINEAR=0
EXPONENTIAL=1

class AHREnvelope:
    """Simple AHR envelope for use with filters"""
    def __init__(self, smax, smin, attack_time, release_time, curve_type=LINEAR):
        self.max = smax
        self.min = smin
        self.attack_time = max(0.001, attack_time)
        self.release_time = max(0.001, release_time)
        self.lerp = synthio.LFO(once=True,
                                waveform=np.array((0,32767),dtype=np.int16))
        if curve_type == LINEAR:
            lerp = self.lerp
        else:         #  EXPONENTIAL
            lerp = synthio.Math(synthio.MathOperation.PRODUCT,
                   	        self.lerp, self.lerp, 1)
        self.env = synthio.Math(synthio.MathOperation.CONSTRAINED_LERP,
                                smin, smax, lerp)

    def press(self):
        """Call this method right before synth.press()"""
        self.env.a = self.smin 
        self.env.b = self.smax
        self.lerp.rate = 1/self.attack_time
        self.lerp.retrigger()
    
    def release(self):
        """Call this method right before synth.release()"""
        self.env.a = self.env.value  # curr val is new start value
        self.env.b = self.smin
        self.lerp.rate = 1/self.release_time
        self.lerp.retrigger()
