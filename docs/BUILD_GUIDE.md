# HexaRover Build Guide

## Introduction

This guide explains how to assemble the HexaRover platform using the provided CAD models, STL files, wiring diagrams, and firmware.

Before beginning, ensure that all required components have been manufactured or procured and that the repository files have been downloaded.

---

# Build Overview

The assembly process consists of five major stages:

1. Fabricate mechanical components
2. Assemble the chassis
3. Install the drive system
4. Wire the electronics
5. Upload firmware and test

Expected build time:

| Skill Level       | Estimated Time |
| ----------------- | -------------- |
| Beginner          | 6–8 Hours      |
| Intermediate      | 3–5 Hours      |
| Experienced Maker | 2–3 Hours      |

---

# Required Tools

## Mechanical Tools

* Screwdriver set
* Needle nose pliers
* Side cutters
* Hex key set
* Measuring scale

## Electronics Tools

* Soldering iron
* Solder wire
* Wire stripper
* Multimeter

## Optional Tools

* Hot glue gun
* Heat shrink tubing
* Cable ties
* Thread locker

---

# Bill of Materials

## Electronics

| Component               | Quantity    |
| ----------------------- | ----------- |
| ESP32 Development Board | 1           |
| Motor Driver Module     | 1           |
| DC Geared Motors        | 2–6         |
| Battery Pack            | 1           |
| Power Switch            | 1           |
| Jumper Wires            | As Required |

## Mechanical

| Component        | Quantity        |
| ---------------- | --------------- |
| 3D Printed Parts | Refer CAD Files |
| Wheels           | 2–6             |
| Fasteners        | As Required     |
| Chassis Panels   | 1 Set           |

---

# Step 1 — Print Components

Locate the STL files in:

```text
CAD/STL/
```

Print all required parts using the recommended settings.

## Recommended Print Settings

| Setting      | Value               |
| ------------ | ------------------- |
| Material     | PLA                 |
| Layer Height | 0.2 mm              |
| Infill       | 25%                 |
| Supports     | Only Where Required |
| Wall Count   | 3                   |

## Verification Checklist

After printing:

* No visible cracks
* Mounting holes are clear
* Connectors fit together
* Parts match assembly drawings

---

# Step 2 — Assemble the Chassis

Using the assembly drawings provided in:

```text
CAD/Assembly/
```

construct the base frame.

## Procedure

1. Lay out all structural parts.
2. Assemble the primary frame.
3. Install reinforcement connectors.
4. Verify alignment.
5. Tighten all structural fasteners.

## Inspection

The chassis should:

* Sit flat on a surface.
* Have no major flexing.
* Maintain symmetrical dimensions.

---

# Step 3 — Install Motor Assemblies

Attach the motor mounts to the chassis.

Install each motor according to the assembly drawings.

## Procedure

1. Insert motors into mounts.
2. Secure using recommended fasteners.
3. Route motor wires inward.
4. Attach wheels.
5. Verify free wheel rotation.

## Verification

Each wheel should:

* Rotate freely.
* Have minimal wobble.
* Remain securely mounted.

---

# Step 4 — Mount Electronics

Locate the electronics mounting locations shown in:

```text
Hardware/Layout/
```

Install:

* ESP32
* Motor Driver
* Power System
* Sensor Modules (Optional)

## Recommended Placement

```text
Front
│
├── Sensors
│
├── ESP32
│
├── Motor Driver
│
└── Battery Pack
│
Rear
```

---

# Step 5 — Wiring

Follow the wiring diagrams located in:

```text
Hardware/Wiring/
```

## Wiring Sequence

### Power System

Connect:

Battery → Switch → Power Distribution

### Controller

Connect:

Power Distribution → ESP32

### Motor Driver

Connect:

Power Distribution → Motor Driver

### Motors

Connect:

Motor Driver → Drive Motors

---

# Step 6 — Firmware Installation

Navigate to:

```text
Firmware/
```

## Setup

1. Install Arduino IDE or PlatformIO.
2. Install ESP32 board package.
3. Open firmware project.
4. Select correct COM port.
5. Upload firmware.

## Verification

Successful upload should display:

```text
HexaRover Boot Complete
WiFi Initialized
Motor Controller Ready
System Ready
```

through the serial monitor.

---

# Step 7 — Initial Testing

Perform the following checks.

## Power Test

Verify:

* ESP32 powers correctly.
* No overheating.
* Stable voltage.

---

## Motor Test

Verify:

* Forward motion
* Reverse motion
* Left turn
* Right turn
* Emergency stop

---

## Communication Test

Verify:

* Bluetooth connection
  or
* Wi-Fi connection

---

# Troubleshooting

## Rover Does Not Power On

Check:

* Battery voltage
* Switch wiring
* Power connections

---

## Motors Do Not Move

Check:

* Driver wiring
* Motor polarity
* Firmware configuration

---

## ESP32 Not Detected

Check:

* USB cable
* Drivers
* COM port selection

---

## Rover Moves Incorrectly

Check:

* Motor orientation
* Wiring polarity
* Wheel installation

---

# Safety Notes

* Never short battery terminals.
* Disconnect power before wiring changes.
* Verify polarity before powering electronics.
* Keep wiring secured away from moving parts.
* Test on a stable surface before deployment.

---

# Build Completion Checklist

* [ ] All printed parts assembled
* [ ] Chassis secured
* [ ] Motors installed
* [ ] Electronics mounted
* [ ] Wiring completed
* [ ] Firmware uploaded
* [ ] Communication verified
* [ ] Motion verified
* [ ] Final inspection completed

---

# Next Steps

After successful assembly, users can:

* Add sensors
* Develop autonomous features
* Integrate cameras
* Build custom payloads
* Modify firmware
* Contribute improvements back to the project

Welcome to the HexaRover community and happy building!

