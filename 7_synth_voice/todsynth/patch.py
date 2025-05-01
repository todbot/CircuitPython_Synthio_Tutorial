
class Patch:
    def __init__(self):
        self.waveform ='saw' # name of waveform
        self._waveform = None  # the actual wave used
        self.detune = 1.001
        # amplitude envelope parameters
        self.attack_time = 0
        self.decay_time = 0.05
        self.release_time = 0.5
        self.sustain_level = 0.8
        self.attack_level = 1.0
        # filter parameters
        self.filter_type = 'lpf'  # or synthio.FilterMode.LOW_PASS,
        self._filter_type = None  # the synthio waveform type
        self.filter_freq = 4000
        self.filter_res = 1.2
        # filter envelope parameters
        self.filter_attack_time = 0.1
        self.filter_release_time = 0.3
        self.filter_freq_min = 0
        
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in self.__dict__.items())
        )
    def __repr__(self):
        return self.__str__()
