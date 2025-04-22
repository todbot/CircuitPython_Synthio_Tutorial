# 4_oscillators_waveforms/code_wavetable.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time
import ulab.numpy as np
import synthio
from synth_setup import synth, keys, knobA
import adafruit_wave

wave_dir = "/wavetable/"  # wavetables from old http://waveeditonline.com/
wavetables = ["BRAIDS01.WAV","DRONE.WAV","SYNTH_VO.WAV","PPG_BES.WAV"]
wavetable_num_samples = 256  # number of samples per wave in wavetable
wti=0  # index into wavetables list

class Wavetable:
    """ A 'waveform' for synthio.Note uses a WAV containing a wavetable
    and provides a scannable wave position."""
    def __init__(self, filepath, wave_len=256):
        self.w = adafruit_wave.open(filepath)
        self.wave_len = wave_len  # how many samples in each wave
        if self.w.getsampwidth() != 2 or self.w.getnchannels() != 1:
            raise ValueError("unsupported WAV format")
        self.waveform = np.zeros(wave_len, dtype=np.int16) # empty buf to fill
        self.num_waves = self.w.getnframes() // self.wave_len
        self.set_wave_pos(0)

    def set_wave_pos(self, pos):
        """Pick which wave to use in the wavetable"""
        pos = min(max(pos, 0), self.num_waves-1)  # constrain
        samp_pos = int(pos) * self.wave_len  # get sample position
        self.w.setpos(samp_pos) # seek to wavetable location
        waveA = np.frombuffer(self.w.readframes(self.wave_len), dtype=np.int16)
        self.waveform[:] = waveA  # copy into buf
        self._wave_pos = pos

wavetable1 = Wavetable(wave_dir+wavetables[wti])  # load up wavetable

midi_note = 45  # A2
note = synthio.Note(synthio.midi_to_hz(midi_note), waveform=wavetable1.waveform)
synth.press(note)  # start note sounding
pos = 0  # last knob position
while True:
    if key := keys.events.get():  # button pushed
        if key.pressed:
            wti = (wti+1) % len(wavetables)  # go to next index
            wavetable1 = Wavetable(wave_dir+wavetables[wti])  # load new wavet
            note.waveform = wavetable1.waveform   # attach to note
    new_pos = (knobA.value / 65535) * wavetable1.num_waves
    pos = int((new_pos*0.5) + pos*0.5)  # filter knob input
    wavetable1.set_wave_pos(pos)   # pick new wavetable
    print("%s: wave num:%d" % (wavetables[wti], pos))
    time.sleep(0.01)
