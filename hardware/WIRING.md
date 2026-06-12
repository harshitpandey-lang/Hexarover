# HexaRover Hardware Wiring Guide

This document describes all electrical connections for the HexaRover platform.

## System Overview

The rover uses a distributed control architecture with three main computational nodes:
- **ESP32**: Main control unit managing motors, servos, and sensors
- **Raspberry Pi 4**: Secondary processor for vision and advanced autonomy
- **FlySky FS-iA6B**: Remote control receiver for manual operation

Power is distributed from a central battery through two main motor drivers and several regulators for different voltage requirements.

## Power Architecture

```
12V LiPo Battery
    │
    ├─ 20A Fuse
    ├─ Main Switch
    │
    ├─→ BTS7960 #1 Motor Driver (12V direct)
    ├─→ BTS7960 #2 Motor Driver (12V direct)
    │
    ├─→ UBEC 5V 15A Regulator (servo power)
    │
    └─→ LM2596 Buck Converter → 5V (ESP32 power)
```

### Battery Specifications
- Type: LiPo 2S-4S configuration (7.4V to 14.8V nominal)
- Recommended capacity: 10000 mAh or higher for extended runtime
- Discharge rate: 50C minimum for sustained motor operation
- Operating temperature: 0-40°C

### Voltage Regulators
- **UBEC (Universal Battery Elimination Circuit)**: Supplies 5V at 15A to servo motors
- **LM2596**: Adjustable step-down converter set to 5V for ESP32 VIN pin

## Motor Control System

The rover uses two independent BTS7960 motor drivers to control left and right motor sets independently, allowing for differential steering and redundancy.

### BTS7960 Motor Driver #1 (Left Side - 3 Motors in Parallel)

**Power Connections:**
```
B+  ──→ +12V from battery
B-  ──→ GND (battery negative)
M+  ──→ Left motor group positive
M-  ──→ Left motor group negative
```

**Control Signals (to ESP32):**
```
RPWM (Forward PWM)  ──→ GPIO 25
LPWM (Reverse PWM)  ──→ GPIO 26
R_EN (Right Enable) ──→ GPIO 33 (tied HIGH)
L_EN (Left Enable)  ──→ GPIO 32 (tied HIGH)
```

### BTS7960 Motor Driver #2 (Right Side - 3 Motors in Parallel)

**Power Connections:**
```
B+  ──→ +12V from battery
B-  ──→ GND (battery negative)
M+  ──→ Right motor group positive
M-  ──→ Right motor group negative
```

**Control Signals (to ESP32):**
```
RPWM (Forward PWM)  ──→ GPIO 27
LPWM (Reverse PWM)  ──→ GPIO 14
R_EN (Right Enable) ──→ GPIO 13 (tied HIGH)
L_EN (Left Enable)  ──→ GPIO 12 (tied HIGH)
```

### Speed Control Logic

PWM Frequency: 5 kHz
PWM Resolution: 8-bit (0-255 values)

**Motor direction commands:**
- Stop: RPWM = 0, LPWM = 0
- Forward: RPWM = speed value, LPWM = 0
- Reverse: RPWM = 0, LPWM = speed value
- Left turn: Left motor reduced, right motor full
- Right turn: Right motor reduced, left motor full

## Servo Steering System

Four MG946R digital servos provide steering control at all four corners for omnidirectional mobility.

**Servo GPIO Assignments:**
| Servo Position | GPIO | Function |
|---|---|---|
| Front Left | 4 | Steering angle |
| Front Right | 5 | Steering angle |
| Rear Left | 18 | Steering angle |
| Rear Right | 19 | Steering angle |

**Power Distribution:**
- All servo power: 5V from UBEC regulator
- All servo GND: Common ground with main power system
- PWM signals: 3.3V logic from ESP32

**Servo Operating Range:**
- Pulse width: 1000-2000 microseconds
- Angle mapping: 45° (full left) → 1000 μs, 90° (center) → 1500 μs, 135° (full right) → 2000 μs
- Frequency: 50 Hz
- All servos synchronized for coordinated steering

## Sensor Connections

### MPU6050 Inertial Measurement Unit (I2C Bus)

Provides 3-axis acceleration and rotation rate measurements for orientation determination.

```
VCC ──→ 3.3V from ESP32
GND ──→ Common GND
SDA ──→ GPIO 21 (ESP32 I2C SDA)
SCL ──→ GPIO 22 (ESP32 I2C SCL)
AD0 ──→ GND (sets I2C address to 0x68)
INT ──→ Optional, not used
```

**Data Output:**
- Roll angle (degrees)
- Pitch angle (degrees)
- Yaw rate (degrees/second)
- Acceleration vectors (X, Y, Z axes)

### NEO-6M GPS Module (UART)

Provides global positioning data and satellite lock information via NMEA protocol.

```
VCC ──→ 5V regulated power
GND ──→ Common GND
RX  ──→ GPIO 17 (ESP32 TX on Serial1)
TX  ──→ GPIO 16 (ESP32 RX on Serial1)
```

**UART Configuration:**
- Baud rate: 9600
- Data bits: 8
- Stop bits: 1
- Parity: None

**Data Output:** NMEA sentences parsed for:
- Latitude/Longitude (6 decimal places)
- Satellite count
- Position fix status

### HC-SR04 Ultrasonic Distance Sensor - Front

Measures distance to obstacles in front of rover.

```
VCC  ──→ 5V regulated power
GND  ──→ Common GND
TRIG ──→ GPIO 2 (3.3V logic)
ECHO ──→ GPIO 34 (with voltage divider: 1kΩ series + 2kΩ to GND)
```

**Voltage Divider for Echo:**
- Reduces 5V sensor output to 3.3V safe for ESP32
- 1kΩ resistor in series from sensor
- 2kΩ resistor to ground

### HC-SR04 Ultrasonic Distance Sensor - Rear

Mirrors front sensor configuration at rear of chassis.

```
VCC  ──→ 5V regulated power
GND  ──→ Common GND
TRIG ──→ GPIO 15 (3.3V logic)
ECHO ──→ GPIO 35 (with voltage divider: 1kΩ series + 2kΩ to GND)
```

**Measurement Range:**
- Minimum: 2 cm
- Maximum: 400 cm
- Update rate: ~60 Hz
- Beam angle: ~15°

## Receiver & Communication

### FlySky FS-iA6B Remote Control Receiver (iBUS Protocol)

Receives wireless commands from remote transmitter using iBUS serial protocol.

```
VCC ──→ 5V regulated power
GND ──→ Common GND
Signal ──→ GPIO 23 (Serial2 RX, iBUS one-wire protocol)
```

**Communication Parameters:**
- Protocol: iBUS (Binary format)
- Baud rate: 115200
- Channels available: 14 (using 3 channels)
- Failsafe timeout: 500 ms

**Channel Mapping:**
- Channel 1: Steering input (1000-2000 μs range, 1500 center)
- Channel 2: Throttle/Speed (1000-2000 μs range, 1500 neutral)
- Channel 5: Autonomous mode toggle (< 1500 = manual, > 1500 = auto)

**Loss of Signal Handling:**
If no iBUS signal received for >500 ms:
- Motors stop immediately
- Servos center (90°)
- Autonomous mode disengages
- LED indicator (if present) blinks

### Raspberry Pi UART Connection

Serial link between ESP32 and Raspberry Pi for telemetry transmission and command reception.

```
ESP32 TX (GPIO 17)  ──→ RPi RX (GPIO 15 / UART0)
ESP32 RX (GPIO 16)  ──→ RPi TX (GPIO 14 / UART0)
GND (ESP32) ────────→ GND (RPi)
```

**UART Parameters:**
- Baud rate: 115200
- Data bits: 8
- Stop bits: 1
- Parity: None
- Handshaking: None

**Telemetry Packet Format:**
```
MODE:MANUAL
DIST_FRONT:123.5
DIST_REAR:95.2
LAT:26.123456
LON:82.654321
ROLL:1.2
PITCH:0.8
YAW:45.5
SATS:12
SIGNAL:98
END
```

Transmission rate: 10 Hz (every 100 ms)

## Complete GPIO Pinout

| GPIO | Function | Type | Voltage | Notes |
|------|----------|------|---------|-------|
| 2 | HC-SR04 Front TRIG | Output | 3.3V | Digital pulse |
| 4 | Servo Front Left | PWM | 3.3V | 50 Hz, 1000-2000 μs |
| 5 | Servo Front Right | PWM | 3.3V | 50 Hz, 1000-2000 μs |
| 12 | BTS7960 #2 L_EN | Output | 3.3V | Always HIGH |
| 13 | BTS7960 #2 R_EN | Output | 3.3V | Always HIGH |
| 14 | BTS7960 #2 LPWM | PWM | 3.3V | 5 kHz reverse |
| 15 | HC-SR04 Rear TRIG | Output | 3.3V | Digital pulse |
| 16 | GPS RX (Serial1) | Input | 3.3V | UART receive |
| 17 | GPS TX (Serial1) | Output | 3.3V | UART transmit |
| 18 | Servo Rear Left | PWM | 3.3V | 50 Hz, 1000-2000 μs |
| 19 | Servo Rear Right | PWM | 3.3V | 50 Hz, 1000-2000 μs |
| 21 | MPU6050 SDA (I2C) | I/O | 3.3V | I2C data line |
| 22 | MPU6050 SCL (I2C) | I/O | 3.3V | I2C clock line |
| 23 | Receiver iBUS | Input | 3.3V | Serial2, 115200 baud |
| 25 | BTS7960 #1 RPWM | PWM | 3.3V | 5 kHz forward |
| 26 | BTS7960 #1 LPWM | PWM | 3.3V | 5 kHz reverse |
| 27 | BTS7960 #2 RPWM | PWM | 3.3V | 5 kHz forward |
| 32 | BTS7960 #1 L_EN | Output | 3.3V | Always HIGH |
| 33 | BTS7960 #1 R_EN | Output | 3.3V | Always HIGH |
| 34 | HC-SR04 Front ECHO | Input | 1.65V | With voltage divider |
| 35 | HC-SR04 Rear ECHO | Input | 1.65V | With voltage divider |

## Typical Current Draw

**During operation:**
- Motors (cruise): 5-8A per driver
- Motors (full load): 15-20A per driver
- Servos (idle): ~50 mA
- Servos (moving): 1-2A combined
- ESP32: 200-400 mA
- Raspberry Pi: 500 mA - 1.5A (depending on camera)
- Sensors: 100-200 mA

**Worst-case total:** 35-40A sustained (requires 5000+ mAh battery capacity)

## Assembly Best Practices

1. **Power Distribution:**
   - Use heavy gauge wire (10 AWG minimum) for main battery lines
   - Keep BTS7960 power cables short and direct
   - Add 10 μF electrolytic + 0.1 μF ceramic capacitors across driver power inputs

2. **Signal Integrity:**
   - Use shielded cables for long sensor runs
   - Keep signal wires away from high-current motor cables
   - Use twisted pairs for differential signals

3. **Grounding:**
   - Star-point ground connection at battery negative
   - Ensure all grounds are bonded together
   - Use separate signal and power grounds where possible

4. **Protection:**
   - 20A automotive fuse on main battery positive line
   - Diode across motor driver logic power for reverse polarity protection
   - Check for shorts with multimeter before first power-up

5. **Testing Steps:**
   - Verify all voltages before connecting ESP32
   - Test motor driver PWM independently first
   - Verify I2C sensors with I2C scanner
   - Test GPS UART with logic analyzer or serial monitor
   - Confirm servo center before attaching mechanisms
