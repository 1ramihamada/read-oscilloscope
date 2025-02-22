# Oscilloscope Data Acquisition and Resistance Calculation

## Overview
This Python script communicates with an oscilloscope using PyVISA to measure voltage values and compute resistance for fabricated sensors based on Ohm's Law. It provides real-time data acquisition, voltage monitoring, and resistance calculations.

## Features
- Connects to an oscilloscope via USB using PyVISA
- Queries and extracts voltage measurements
- Computes sensor resistance using Ohm's Law
- Performs continuous measurement of voltage parameters
- Includes error handling for robust communication

## Requirements
- Python 3.x
- PyVISA (`pip install pyvisa`)
- PyVISA-Py (for USB communication, `pip install pyvisa-py`)
- A supported oscilloscope with USB connection

## Installation
1. Clone this repository or download the script:
   ```sh
   git clone https://github.com/your-repo/oscilloscope-resistance.git
   cd oscilloscope-resistance
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure your oscilloscope is connected via USB and recognized by PyVISA:
   ```sh
   pyvisa-info
   ```

## Usage
Run the script to initiate communication with the oscilloscope and start continuous measurements:
```sh
python oscilloscope_resistance.py
```

### Functions
#### 1. `calculate_resistance(inst, current)`
Reads the voltage from the oscilloscope and calculates resistance:
```python
resistance = calculate_resistance(inst, 0.01)  # 10mA current
```

#### 2. `check_communication(inst)`
Verifies connectivity with the oscilloscope by querying its identity and operational status.

#### 3. `check_inr(inst)`
Queries the oscilloscope's internal register.

#### 4. `continuous_dc_average(inst)`
Continuously monitors the DC mean voltage from Channel 1.

#### 5. `continuous_measurement(inst)`
Measures RMS and MEAN voltages from Channels 1 & 2, then calculates sensor resistance.

### Example Output
```
RMS_C1: 25.00 mV | MEAN_C1: 24.50 mV | RMS_C2: 10.00 mV | MEAN_C2: 9.50 mV | R_SENSOR: 25.79 Ω
```

## Error Handling
- Handles VISA I/O errors for oscilloscope communication failures.
- Prevents division by zero errors when calculating resistance.
- Graceful exit on `KeyboardInterrupt` (Ctrl+C).

## License
This project is licensed under the MIT License.
