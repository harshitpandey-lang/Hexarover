#!/usr/bin/env python3
"""
HexaRover installation and dependency setup
Run this on Raspberry Pi to install all required packages
"""

import subprocess
import sys

def run_command(cmd, description):
    """Run a shell command and report status"""
    print(f"\n[*] {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"[✓] {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[✗] {description} - Failed")
        return False

def main():
    print("=== HexaRover Raspberry Pi Setup ===\n")
    
    if sys.platform != "linux":
        print("[!] Warning: This script is designed for Raspberry Pi (Linux)")
    
    # Update system
    run_command("sudo apt-get update", "Updating package list")
    
    # Install system dependencies
    run_command("sudo apt-get install -y python3-pip", "Installing pip")
    run_command("sudo apt-get install -y python3-cv2", "Installing OpenCV")
    run_command("sudo apt-get install -y python3-serial", "Installing serial support")
    run_command("sudo apt-get install -y libatlas-base-dev", "Installing math libraries")
    
    # Install Python packages
    run_command("pip3 install opencv-python", "Installing OpenCV Python package")
    run_command("pip3 install pyserial", "Installing PySerial")
    run_command("pip3 install numpy", "Installing NumPy")
    
    # Enable UART on Raspberry Pi
    print("\n[!] Make sure to enable UART in raspi-config:")
    print("    sudo raspi-config")
    print("    -> Interface Options -> Serial Port -> Enable")
    print("    -> Reboot when done")
    
    print("\n[✓] Setup complete!")
    print("\nTo run HexaRover:")
    print("    python3 firmware/src/main.py")

if __name__ == "__main__":
    main()
