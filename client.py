#!/usr/bin/env python3
import logging
import queue
import time
import csv
from threading import Thread
from pymodbus.client import ModbusTcpClient

# Set up logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Function to read data from the server and add it to the queue
def read_and_enqueue(client, data_queue):
    while True:
        # Read holding registers from address 0 with a length of 2, slave id is passed via `slave`
        result = client.read_holding_registers(0, count=2, slave=1)
        if result.isError():
            log.error("Error reading holding registers")
        else:
            data = result.registers
            log.debug(f"Read data: {data}")
            data_queue.put(data)  # Add the data to the queue
        time.sleep(0.2)

# Function to dump data to CSV when the queue reaches a threshold
def dump_to_csv(data_queue, threshold=5):
    while True:
        if data_queue.qsize() >= threshold:
            # Generate a new filename with a timestamp or counter
            filename = f'dumps/mock_data_dump_{int(time.time())}.csv'
            
            # Open the new file for writing
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                
                # Dump all data in the queue to the CSV file
                while not data_queue.empty():
                    data = data_queue.get()
                    writer.writerow([time.time(), *data])  # Write timestamp and data to CSV
                    log.debug(f"Data dumped to CSV: {data}")
                    
            time.sleep(2)  # Delay before the next check

def run_tcp_client():
    # Create a queue to store received data
    data_queue = queue.Queue()

    # Configure the client and connect to the server
    client = ModbusTcpClient('127.0.0.1', port=5020)
    client.connect()

    # Start the reading thread
    read_thread = Thread(target=read_and_enqueue, args=(client, data_queue))
    read_thread.daemon = True
    read_thread.start()

    # Start the dumping thread
    dump_thread = Thread(target=dump_to_csv, args=(data_queue,))
    dump_thread.daemon = True
    dump_thread.start()

    # Keep the main thread alive to allow background threads to work
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()

if __name__ == "__main__":
    run_tcp_client()
