# code_spi_dac_demo.py -- Full SPI DAC demonstration
# part of todbot circuitpython synthio tutorial
# 12 Sep 2024 - @todbot / Tod Kurt
#
# This example demonstrates the SPI DAC functionality with interactive controls
#
# Hardware needed:
# - Raspberry Pi Pico (or compatible)
# - MCP4922 or compatible SPI DAC
# - 2 potentiometers (10kΩ)
# - 1 button
# - Audio output filtering and connectors
#
import time
import random
import math
from synth_setup_spi import synth, keys, knobA, knobB, update_audio

# musical scales for the demo
pentatonic = (60, 62, 64, 67, 69)  # C pentatonic
blues = (60, 63, 65, 66, 67, 70)   # C blues scale
major = (60, 62, 64, 65, 67, 69, 71)  # C major

scales = [pentatonic, blues, major]
scale_names = ["Pentatonic", "Blues", "Major"]
current_scale = 0

# demo parameters
base_freq = 220.0  # Base frequency for oscillation
last_note_time = 0
note_duration = 0.5
current_notes = []

print("SPI DAC Synthio Demo")
print("Knob A: Frequency/Pitch")
print("Knob B: Filter/Modulation")
print("Button: Change scale")
print()

def knob_to_float(knob):
    """Convert knob reading to 0.0-1.0 range"""
    return knob.value / 65535

def play_random_note(scale, duration=0.5):
    """Play a random note from the given scale"""
    note = random.choice(scale)
    synth.press(note)
    current_notes.append((note, time.monotonic() + duration))
    return note

def cleanup_notes():
    """Release notes that have finished playing"""
    global current_notes
    current_time = time.monotonic()
    for note, end_time in current_notes[:]:  # Copy list to iterate safely
        if current_time >= end_time:
            synth.release(note)
            current_notes.remove((note, end_time))

def update_synthesis():
    """Update synthesis parameters based on knob positions"""
    knobA_val = knob_to_float(knobA)
    knobB_val = knob_to_float(knobB)
    
    # KnobA controls global pitch bend
    pitch_bend = (knobA_val - 0.5) * 2.0  # -1.0 to 1.0
    # Convert to cents (1200 cents = 1 octave)
    pitch_cents = pitch_bend * 200  # +/- 200 cents
    
    # Apply pitch bend to all active notes
    for note_info in synth.pressed:
        if hasattr(note_info, 'bend'):
            note_info.bend = pitch_cents / 1200.0  # Convert cents to ratio
    
    # KnobB controls filter frequency (if we add filtering later)
    filter_freq = 200 + (knobB_val * 8000)  # 200Hz to 8200Hz
    
    return knobA_val, knobB_val

# Main demo loop
last_update = time.monotonic()
update_interval = 1.0 / 100.0  # 100Hz update rate

print(f"Starting with {scale_names[current_scale]} scale")

while True:
    current_time = time.monotonic()
    
    # Update audio processing (CRITICAL for SPI DAC)
    update_audio()
    
    # Check for button presses to change scale
    key_event = keys.events.get()
    if key_event and key_event.pressed:
        current_scale = (current_scale + 1) % len(scales)
        print(f"Switched to {scale_names[current_scale]} scale")
        # Release all current notes when changing scale
        synth.release_all()
        current_notes.clear()
    
    # Regular updates at controlled rate
    if current_time - last_update >= update_interval:
        last_update = current_time
        
        # Update synthesis parameters
        knobA_val, knobB_val = update_synthesis()
        
        # Clean up finished notes
        cleanup_notes()
        
        # Play new notes based on timing and parameters
        if current_time - last_note_time >= note_duration:
            # Vary note duration based on knobB
            note_duration = 0.2 + (knobB_val * 0.8)  # 0.2s to 1.0s
            
            # Play a note if not too many are already playing
            if len(current_notes) < 3:
                note = play_random_note(scales[current_scale], note_duration)
                print(f"Playing note {note}, duration {note_duration:.2f}s")
            
            last_note_time = current_time
    
    # Small delay to prevent overwhelming the system
    time.sleep(0.001)  # 1ms delay