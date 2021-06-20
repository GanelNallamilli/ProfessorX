#https://pimylifeup.com/raspberry-pi-accelerometer-adxl345/
#sudo apt-get update
#sudo apt-get upgrade
#sudo raspi-config
#sudo reboot
#sudo apt-get install python3-dev python3-pip python3-smbus i2c-tools -y
#sudo i2cdetect -y 1
#sudo pip3 install adafruit-circuitpython-ADXL34x
import time
import board
import busio
import adafruit_adxl34x
import numpy

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

while True:
    accelerationValues = "%f %f %f"%accelerometer.acceleration
    print(accelerationValues)
    accelerationVector = np.array(float(accelerationValues.split()))
    accelerationMagni = np.sqrt(accelerationVector[0]**2+accelerationVector[1]**2+accelerationVector[2]**2)


    time.sleep(1)