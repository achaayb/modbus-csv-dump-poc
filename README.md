# modbus-data-dump-poc

This is a proof of concept (POC) for collecting sensor data via the Modbus protocol and saving it to a CSV file. It was designed with the SIEMENS PAC3220 in mind but uses a local mock server to simulate the device for testing purposes.

The project demonstrates:
- Setting up a mock ModbusTCP server to emulate a sensor device.
- Running a client script that continuously reads data from the server and dumps it into a CSV file when certain thresholds are met.

The client script can be adapted to meet your requirements, such as adjusting the read frequency or modifying the CSV handling logic.

---

## Modbus and Registers

Modbus is a protocol used to exchange data between devices. It organizes data into **registers**:
- **Holding Registers (HR):** Writable/readable data, often used for configuration or measurements.
- **Input Registers (IR):** Read-only data, typically used for live sensor values.

Each register holds a 16-bit value and is identified by an address. For example:
- Address 0: Voltage
- Address 1: Current
- Address 2: Power

## Notes

Registers dont hold historical values, which means a continuous read is needed.

The register map for a specific device like the PAC3220 provides these details.
