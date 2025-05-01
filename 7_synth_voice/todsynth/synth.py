import random
import ulab.numpy as np
import synthio

from todsynth import Note
from todsynth import Patch

NUM = 128    # number of samples in oscillator waveforms
VOL = 32000  # volume (amplitude) of samples, max is +32767

FILTER_TYPES = {
    'lpf' : synthio.FilterMode.LOW_PASS,
    'hpf' : synthio.FilterMode.HIGH_PASS,
    'bpf' : synthio.FilterMode.BAND_PASS,
    }

WAVEFORMS = {
    'saw' : np.linspace(VOL, -VOL, num=NUM, dtype=np.int16),
    'sine': np.array(np.sin(np.linspace(0, 2*np.pi, NUM, endpoint=False)) * VOL, dtype=np.int16),
    'square': np.concatenate((np.ones(NUM // 2, dtype=np.int16) * VOL,
                              np.zeros(NUM // 2, dtype=np.int16) * -VOL)),
    'noise': np.array([random.randint(-VOL, VOL) for i in range(NUM)], dtype=np.int16),
}

class Synth:
    
    def __init__(self, synth:synthio.Synthesizer, patch=None):
        self.synth = synth
        self.load_patch(patch)
        self.notes_pressed = {}
        
    def __repr__(self):
        return "Synth(",self.patch,")"

    def load_patch(self, patch):
        self.patch = patch or Patch()
        self.patch._waveform = WAVEFORMS[self.patch.waveform]
        self.patch._filter_type = FILTER_TYPES[self.patch.filter_type]

    def set_parameter(self, name, value):
        """Set a patch parameter by name"""
        pass

    def is_pressed(self, midi_note):
        return self.notes_pressed.get(midi_note, None)
    
    def add_note(self, midi_note, note:Note):
        self.notes_pressed[midi_note] = note
        
    def del_note(self, midi_note):
        self.notes_pressed[midi_note] = None


    def press(self, midi_note, velocity=127):
        """override this"""
        if self.is_pressed(midi_note):
            self.release(midi_note, 0)  # we're at max notes
        tnote = Note(synthio.Note(synthio.midi_to_hz(midi_note)))
        self.synth.press(tnote.note)
        self.add_note(midi_note, tnote)

    def release(self, midi_note, velocity=127):
        if tnote := self.is_pressed(midi_note):
            self.synth.release(tnote.note)
        self.del_note(midi_note)

    def control_change(self, cc_num, cc_val):
        pass

    def bend(self, amount):
        pass
    
    def connect_param_to_cc(self, name, cc_num, amount):
        pass

    def disconnect_param_to_cc(self, name, cc_num):
        pass
