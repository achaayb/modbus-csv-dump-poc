#!/usr/bin/env python3
import logging
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from threading import Thread

# Set up logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Constants
UPDATE_INTERVAL = 0.2
START_ADDRESS = 0
HOST = "0.0.0.0"
PORT = 5020


# Function to continuously update data in the server
def update_server_data(context: ModbusServerContext):
    global START_ADDRESS
    global UPDATE_INTERVAL
    while True:
        """
        Updates the holding registers (function code 3) of the specified Modbus slave.

        The `setValues` method allows you to write data to the Modbus slave device.
        In this case, it writes values to the holding registers,
        which are typically used to store configuration or process data.

        Parameters:
            slave_id (int): The Modbus slave address (e.g., 0x01 for slave 1).
            function_code (int): The Modbus function code (e.g., 3 for reading/writing holding registers).
            start_address (int): The starting address of the register to write to.
            values (list): A list of values to write to the registers.
        """
        context[0x01].setValues(3, START_ADDRESS, [100, 200])
        log.debug(f"Updated holding registers with mock data: [100, 200]")
        time.sleep(UPDATE_INTERVAL)

def run_tcp_server():
    # Create a simple Modbus datastore
    store = ModbusSlaveContext()
    context = ModbusServerContext(slaves=store, single=True)

    # Start a separate thread to continuously update data
    update_thread = Thread(target=update_server_data, args=(context,))
    update_thread.daemon = True
    update_thread.start()

    # Gracefully handle shutdown
    try:
        StartTcpServer(context, address=(HOST,PORT))
    except KeyboardInterrupt:
        log.info("Shutting down server...")

if __name__ == "__main__":
    run_tcp_server()
