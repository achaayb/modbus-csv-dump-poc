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

# Function to continuously update data in the server
def update_server_data(context):
    while True:
        # Simulate changing data for holding registers
        context[0x01].setValues(3, 0, [100, 200])  # Update holding registers with mock data
        log.debug(f"Updated holding registers with mock data: [100, 200]")
        time.sleep(0.2)

def run_tcp_server():
    # Create a simple Modbus datastore
    store = ModbusSlaveContext()
    context = ModbusServerContext(slaves=store, single=True)

    # Start a separate thread to continuously update data
    Thread(target=update_server_data, args=(context,)).start()

    # Start the TCP server
    StartTcpServer(context, address=("0.0.0.0", 5020))

if __name__ == "__main__":
    run_tcp_server()
