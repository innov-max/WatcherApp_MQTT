# WatcherApp_MQTT
A logging service application that used MQTT to report the connection status of the network.

.. _mqtt_client:

MQTT Client
============

This module defines an MQTT client that connects to an MQTT broker and sends network statistics.

Prerequisites
-------------
This code requires `paho-mqtt`_ library to be installed.

.. _paho-mqtt: https://pypi.org/project/paho-mqtt/

How to Run
----------
To run this module, follow these steps:

1. Install `paho-mqtt`_ library.
2. Set the `broker_address`, `broker_port`, and `client_id` variables in the code to match your MQTT broker settings.
3. Run the following command in the terminal:

   .. code-block:: sh

      python mqtt_client.py

   The client will connect to the broker and start sending network statistics.

How to Stop
-----------
To stop the MQTT client, press `Ctrl+C` in the terminal.

Code Documentation
------------------
.. code-block:: python

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

The code first imports the necessary libraries, `paho.mqtt.client` and `time`. The `broker_address`, `broker_port`, and `client_id` variables are then defined. Two callback functions, `on_connect` and `on_disconnect`, are defined to handle connection and disconnection events.

A new MQTT client instance is then created and the callback functions and network statistics variables are set. The client is connected to the broker and the loop is started using `client.loop_forever()`.

If the client loses and then regains connection to the broker, network statistics are printed.

.. note::
   This code is designed to run indefinitely until manually stopped.
