import adafruit_sht4x
import board
import time
from flask import Flask
app = Flask(__name__)
i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_sht4x.SHT4x(i2c)
print("Found SHT4x with serial number", hex(sht.serial_number))

sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

@app.route('/metrics')
def sht40_metrics():
    temperature, humidity = sht.measurements
    return "temperature {}\nhumidity {}".format(temperature, humidity)
