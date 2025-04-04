# 4_oscillators_wavetables/wavetable.py
# simple wavetable class for synthio
#
import ulab.numpy as np
import synthio
import adafruit_wave

class Wavetable:
    """ A 'waveform' for synthio.Note that uses a wavetable w/ a scannable wave position."""    
    def __init__(self, filepath, wave_len=256):
        self.w = adafruit_wave.open(filepath)
        self.wave_len = wave_len  # how many samples in each wave
        if self.w.getsampwidth() != 2 or self.w.getnchannels() != 1:
            raise ValueError("unsupported WAV format")
        self.waveform = np.zeros(wave_len, dtype=np.int16)  # empty buffer we'll copy into
        self.num_waves = self.w.getnframes() // self.wave_len
        self._wave_pos = 0

    @property
    def wave_pos(self): return self._wave_pos
    
    @wave_pos.setter
    def wave_pos(self, pos):
        """Pick where in wavetable to be, morphing between waves"""
        pos = min(max(pos, 0), self.num_waves-1)  # constrain
        samp_pos = int(pos) * self.wave_len  # get sample position
        self.w.setpos(samp_pos)  
        waveA = np.frombuffer(self.w.readframes(self.wave_len), dtype=np.int16)
        self.w.setpos(samp_pos + self.wave_len)  # one wave up
        waveB = np.frombuffer(self.w.readframes(self.wave_len), dtype=np.int16)
        pos_frac = pos - int(pos)  # fractional position between wave A & B
        self.waveform[:] = Wavetable.lerp(waveA, waveB, pos_frac) # mix waveforms A & B
        self._wave_pos = pos

    # mix between values a and b, works with numpy arrays too, t ranges 0-1
    def lerp(a, b, t):  return (1-t)*a + t*b
