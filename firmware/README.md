# Firmware Structure

This directory contains the complete ESP32 firmware for HexaRover.

## Build & Upload

Using PlatformIO:
```bash
cd firmware
pio run -e esp32doit-devkit-v1
pio run -e esp32doit-devkit-v1 --target upload
```

Or Arduino IDE:
- Open `src/main.cpp`
- Select board: ESP32 DevKit V1
- Select port and upload

## File Organization

```
firmware/
├── platformio.ini          # Build configuration
├── src/
│   ├── main.cpp            # Main firmware entry point
│   ├── motor_controller.h/cpp   # BTS7960 motor driver interface
│   ├── servo_controller.h/cpp   # MG946R servo interface  
│   ├── sensor_manager.h/cpp     # IMU, GPS, ultrasonic handling
│   ├── receiver.h/cpp          # FlySky FS-iA6B iBUS receiver
│   ├── telemetry.h/cpp         # Telemetry to Raspberry Pi
│   └── main.py             # Raspberry Pi control app
├── setup.py                # RPi dependency installer
└── WIRING.md              # Hardware connection guide
```

## Module Overview

### Motor Controller
Manages dual BTS7960 motor drivers with PWM speed control. Supports independent left/right control and synchronized forward/reverse motion.

### Servo Controller  
Controls four MG946R steering servos via PWM. All servos synchronized for unified steering angle.

### Sensor Manager
Aggregates data from:
- MPU6050 IMU (roll, pitch, yaw via I2C)
- NEO-6M GPS (coordinates, satellite count via UART1)
- HC-SR04 ultrasonic sensors (front & rear distance via GPIO)

### Receiver Manager
Decodes FlySky FS-iA6B iBUS protocol at 115200 baud. Extracts 14 channels with failsafe detection on signal loss.

### Telemetry Manager
Sends formatted telemetry packets to Raspberry Pi at 10 Hz containing mode, distances, GPS, and orientation data.

## Key Features

- **Modular Class Architecture**: Each subsystem is independent and reusable
- **Failsafe Logic**: Automatic stop & center steering on receiver signal loss
- **Autonomous Mode**: Obstacle avoidance with front distance sensor
- **Live Telemetry**: Continuous sensor streaming to Raspberry Pi
- **Debug Output**: Serial console logging for development

## Compilation Requirements

- PlatformIO IDE or Arduino IDE
- ESP32 Board Support Package
- Libraries:
  - ESP32Servo
  - MPU6050
  - TinyGPS++
  - Adafruit-BusIO

All handled automatically by platformio.ini
