from PiicoDev_RGB import PiicoDev_RGB, wheel
from PiicoDev_CAP1203 import PiicoDev_CAP1203
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function

leds = PiicoDev_RGB() # initialise the LED module with conservative default brightness
# leds.setBrightness(127) # 0-255 set the global brightness to half

# pre-define some colours
red = [255,0,0]
green = [0,255,0]
blue = [0,0,255]
yellow = [255,255,0]
magenta = [255,0,255]
cyan = [0,255,255]
white = [255,255,255]
black = [0,0,0]

touchSensor = PiicoDev_CAP1203()

while True:
    # Example: Display touch-pad statuses
    leds.clear()
    status = touchSensor.read()
    if status[1] == 1:
        leds.setPixel(0, red)
        print("R")
    if status[2] == 1:
        leds.setPixel(1, green)
        print("W")
    if status[3] == 1:
        leds.setPixel(2, blue)
        print("Y")
    sleep_ms(100)
    leds.show()