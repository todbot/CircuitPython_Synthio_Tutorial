# test_spi_dac.py -- Basic test for SPI DAC functionality
# part of todbot circuitpython synthio tutorial
# 12 Sep 2024 - @todbot / Tod Kurt
#
# This is a simple test to verify SPI DAC functionality
# Run this on actual hardware to test SPI DAC audio output
#
import time
import board
import busio
from audiobusio_spi import SPIOut, DAC_MCP4922

print("Testing SPI DAC functionality...")

# Initialize SPI
try:
    spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)
    print("SPI bus initialized")
except Exception as e:
    print(f"SPI initialization failed: {e}")
    raise

# Create SPI DAC
try:
    dac = SPIOut(spi=spi,
                 cs=board.GP20,
                 dac_type=DAC_MCP4922,
                 sample_rate=22050,
                 channel_count=2,
                 ldac=board.GP21)
    print("SPI DAC created successfully")
except Exception as e:
    print(f"SPI DAC creation failed: {e}")
    raise

# Test basic DAC output with a simple pattern
print("Testing basic DAC output...")
try:
    # Write some test values to verify DAC communication
    test_values = [0, 1024, 2048, 3072, 4095]  # Range of DAC values
    
    for i, value in enumerate(test_values):
        print(f"Writing test value {i+1}/5: {value}")
        dac._write_dac_sample(value, value)
        time.sleep(0.1)
    
    print("Basic DAC test completed")
    
except Exception as e:
    print(f"DAC test failed: {e}")

# Test audio processing loop
print("Testing audio update loop...")
try:
    # Create a dummy audio source for testing
    class DummyAudioSource:
        def __init__(self):
            self.sample_rate = 22050
    
    dummy_source = DummyAudioSource()
    dac.play(dummy_source)
    
    # Run update loop for a short time
    start_time = time.monotonic()
    update_count = 0
    
    while time.monotonic() - start_time < 2.0:  # Run for 2 seconds
        dac.update()
        update_count += 1
        time.sleep(0.001)  # Small delay
    
    dac.stop()
    print(f"Audio update test completed - {update_count} updates in 2 seconds")
    
except Exception as e:
    print(f"Audio update test failed: {e}")

print("SPI DAC test completed!")
print("If you heard audio during the test, the SPI DAC is working correctly.")