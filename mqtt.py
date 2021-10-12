import os
import time
import sys
import adafruit_sht4x
import board
import time
import paho.mqtt.client as mqtt
import json

MQTT_BROKER_HOST = 'hostname'

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL = 2

i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))

sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

next_reading = time.time()
client = mqtt.Client()

# Set access token
client.username_pw_set(
    username="mqtt", password="mqttpass")

# Connect to the MQTT Broker using default MQTT port and 60 seconds keepalive interval
client.connect(MQTT_BROKER_HOST, 1883, 60)

client.loop_start()

try:
    while True:
        temperature, humidity = sht.measurements
        humidity = round(humidity, 2)
        temperature = round(temperature, 2)
        print(u"Temperature: {:g}\u00b0C, Humidity: {:g}%".format(
            temperature, humidity))

        # Sending humidity and temperature data to the MQTT Broker
        client.publish('/home/basement/sht40',
                       json.dumps({"temperature": temperature, "humidity": humidity}), 1)

        next_reading += INTERVAL
        sleep_time = next_reading-time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
