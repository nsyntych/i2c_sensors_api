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


@app.route('/sht40')
def sht40_metrics():
    temperature, humidity = sht.measurements
    return "sht40_temperature {}\nsht40_humidity {}".format(temperature, humidity)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
