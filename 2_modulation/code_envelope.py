# 2_modulation/code_envelope.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
from synth_setup import synth, knobA, knobB
while True:
    synth.envelope = synthio.Envelope(
        attack_level = 0.8, sustain_level = 0.8,
        attack_time = 2 * (knobA.value/65535),  # range from 0-2 seconds
        release_time = 2 * (knobB.value/65535),  # range from 0-2 seconds
        )
    midi_note = random.randint(48,60)
    synth.press(midi_note)
    time.sleep(synth.envelope.attack_time)  # wait enough time to hear the attack finish
    synth.release(midi_note)
    time.sleep(synth.envelope.release_time)  # wait enough time to hear the release finish
