import paho.mqtt.client as mqtt
import time

# Define the broker details
broker_address = "localhost"
broker_port = 1883
client_id = "myclient"

# Define the callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker!")
        client.connected_time = time.time()
        client.retries = 0
    else:
        print("Connection to MQTT broker failed. Retrying...")
        client.retries += 1
        time.sleep(5)
        client.connect(broker_address, broker_port)
        
def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker. Retrying...")
    client.disconnected_time = time.time()
    time.sleep(5)
    client.connect(broker_address, broker_port)

# Create a new MQTT client instance
client = mqtt.Client(client_id=client_id)

# Set the callback functions and network statistics variables
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.disconnected_time = 0
client.connected_time = 0
client.retries = 0

# Connect to the broker and start the loop
client.connect(broker_address, broker_port)
client.loop_forever()

# Send network statistics
if client.disconnected_time != 0 and client.connected_time != 0:
    print("Time lost connection: ", client.disconnected_time)
    print("Time got connection: ", client.connected_time)
    print("Number of retries: ", client.retries)
  