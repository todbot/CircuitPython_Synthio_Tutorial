# SPI DAC Support for CircuitPython Synthio

This directory contains an implementation of SPI DAC support for use with CircuitPython's `synthio` module. This provides an alternative to I2S DACs for audio output.

## Overview

The SPI DAC implementation allows you to use common SPI-based Digital-to-Analog Converters for audio output with synthio. This is useful when:

- You want to use a different DAC than the standard I2S options
- Your microcontroller doesn't have I2S support
- You want more control over the audio output timing
- You're working with existing SPI DAC hardware

## Supported DAC Chips

The implementation currently supports these SPI DAC chips:

- **MCP4922**: 12-bit dual channel DAC (recommended)
- **MCP4912**: 10-bit dual channel DAC
- **TLV5618**: 12-bit dual channel DAC

Additional DAC chips can be easily added by implementing the appropriate command format in the `spi_dac.py` module.

## Files

- `audiobusio_spi.py` - Main SPI DAC module implementing the audio interface (improved version)
- `spi_dac.py` - Original SPI DAC module with basic functionality
- `synth_setup_spi.py` - Modified synth setup using SPI DAC instead of I2S
- `code_helloboop_spi.py` - Example "hello world" program using SPI DAC
- `code_spi_dac_demo.py` - Interactive demo with scales and controls
- `test_spi_dac.py` - Basic test script to verify SPI DAC functionality

## Hardware Setup

### Basic Wiring (MCP4922 example)

```
Pico Pin    MCP4922 Pin    Description
--------    -----------    -----------
GP18        SCK            SPI Clock
GP19        SDI            SPI Data In
GP20        CS             Chip Select
GP21        LDAC           Load DAC (optional)
3.3V        VDD            Power
3.3V        VREF           Reference Voltage
GND         VSS            Ground
-           VOUTA          Left Audio Output
-           VOUTB          Right Audio Output
```

### External Components

- Output filtering capacitors (100nF ceramic + 10-100µF electrolytic per channel)
- Pull-up resistor on LDAC pin (10kΩ to 3.3V) if not using the LDAC control pin
- Audio output connectors (3.5mm jack, RCA jacks, etc.)

## Usage

### Basic Setup

```python
import board
import busio
from audiobusio_spi import SPIOut, DAC_MCP4922

# Initialize SPI
spi = busio.SPI(clock=board.GP18, MOSI=board.GP19)

# Create SPI DAC audio output (improved interface)
audio = SPIOut(spi=spi, 
               cs=board.GP20, 
               dac_type=DAC_MCP4922,
               sample_rate=22050,
               channel_count=2,
               ldac=board.GP21)
```

### With Synthio

```python
from synth_setup_spi import synth, update_audio

# Play a note
synth.press(60)  # Middle C

# In your main loop, call update_audio() regularly
while True:
    # Your code here
    update_audio()  # Important: keeps audio flowing
```

## Important Notes

### Performance Considerations

- The SPI DAC implementation requires regular calls to `update_audio()` in your main loop
- Audio quality depends on how frequently and consistently you call the update function
- For best results, avoid long-running operations that block the main loop
- Consider the SPI clock speed - faster is generally better for audio quality

### Limitations

- This is a software-based audio implementation, so it's more CPU intensive than hardware I2S
- Audio latency may be higher than with I2S DACs
- Sample rate accuracy depends on main loop timing
- Limited to the bit depth of your chosen DAC chip

### Audio Quality Tips

- Use the highest bit depth DAC available (12-bit recommended)
- Keep SPI clock speed high (10 MHz or more if supported)
- Use LDAC pin for simultaneous stereo channel updates
- Add appropriate output filtering to reduce noise
- Minimize other processing in the main loop for consistent timing

## Adding New DAC Chips

To add support for a new SPI DAC chip:

1. Add a new constant for the DAC type (e.g., `DAC_MY_CHIP = const(3)`)
2. Add configuration in `__init__()` for the new chip's specifications
3. Implement a new `_write_my_chip()` method with the proper SPI command format
4. Add the new chip to the `_write_dac_sample()` method

## Example DAC Command Formats

### MCP4922 (12-bit)
```
Bit 15:    A/B select (0=A, 1=B)
Bit 14:    BUF (buffer control)
Bit 13:    GA (gain select)
Bit 12:    SHDN (shutdown control)
Bits 11-0: Data
```

### TLV5618 (12-bit)
```
Bits 15-14: DAC select (00=A, 01=B)
Bit 13:     Speed select
Bit 12:     Power down
Bits 11-0:  Data
```

## Troubleshooting

### No Audio Output
- Check SPI wiring and connections
- Verify DAC power supply (3.3V)
- Ensure `update_audio()` is being called regularly
- Check that audio output filtering is properly connected

### Distorted Audio
- Reduce audio levels in your synth setup
- Check for proper grounding
- Verify SPI timing (try lower SPI clock speed)
- Ensure adequate power supply decoupling

### Poor Audio Quality
- Increase the frequency of `update_audio()` calls
- Use a higher bit depth DAC
- Add better output filtering
- Minimize other processing in the main loop

## Contributing

To improve this SPI DAC implementation:

- Add support for additional DAC chips
- Improve audio buffering and timing
- Add interrupt-based or DMA-based processing
- Optimize for specific microcontroller architectures

## License

This SPI DAC implementation is part of the CircuitPython Synthio Tutorial and follows the same license terms.