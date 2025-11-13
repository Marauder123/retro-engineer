"""
This Raspberry Pi Pico MicroPython code was developed by newbiely.com
This Raspberry Pi Pico code is made available for public use without any restriction
For comprehensive instructions and wiring diagrams, please visit:
https://newbiely.com/tutorials/raspberry-pico/raspberry-pi-pico-switch
"""

from DIYables_MicroPython_Button import Button
import time

# Initialize the on/off switch connected to GPIO pin GP1 of the Raspberry Pi Pico
switch = Button(1)

# Set debounce time to 50 milliseconds
switch.set_debounce_time(50)

while True:
    switch.loop()  # Update the button state

    if switch.is_pressed():
        print("The switch: OFF -> ON")

    if switch.is_released():
        print("The switch: ON -> OFF")
