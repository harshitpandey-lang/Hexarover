#include "telemetry.h"

TelemetryManager::TelemetryManager() {}

void TelemetryManager::init() {
  // Initialize Serial1 for Raspberry Pi communication
  // Using GPIO 16 (RX) and GPIO 17 (TX)
  Serial1.begin(115200, SERIAL_8N1, RX_PIN, TX_PIN);
  Serial.println("[Telemetry] UART to Raspberry Pi initialized on pins 16/17");
}

void TelemetryManager::send(String data) {
  // Send telemetry string to Raspberry Pi
  Serial1.print(data);
}
