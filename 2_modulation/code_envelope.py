# 2_modulation/code_envelope.py
# part of todbot circuitpython synthio tutorial
# 10 Feb 2025 - @todbot / Tod Kurt
#
import time, random
import synthio
from synth_setup import synth, knobA, knobB
while True:
    amp_env = synthio.Envelope(
        attack_level = 0.8, sustain_level = 0.8,
        attack_time = 1 * (knobA.value/65535),  # range from 0-1 seconds
        release_time = 2 * (knobB.value/65535),  # range from 0-2 seconds
    )
    synth.envelope = amp_env
    print("attack_time:%.2f release_time:%.2f" %
          (amp_env.attack_time, amp_env.release_time))
    midi_note = random.randint(48,60)
    synth.press(midi_note)
    time.sleep(amp_env.attack_time)  # wait to hear the attack finish
    synth.release(midi_note)
    # wait enough time to hear the release finish, but with some overlap
    time.sleep(max(amp_env.release_time * 0.75, 0.1))  # 0.1 sec smallest sleep
