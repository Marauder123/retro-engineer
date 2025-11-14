from machine import Pin
import utime

# Define the GPIO pin the button is connected to
button_pin = Pin(15, Pin.IN, Pin.PULL_DOWN)

pilot_pin = Pin(16, Pin.IN, Pin.PULL_DOWN)
science_pin = Pin(17, Pin.IN, Pin.PULL_DOWN)
weapon_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)

power_down_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
power_up_pin = Pin(1, Pin.IN, Pin.PULL_DOWN)


while True:
    if button_pin.value() == 1:  # Check if the YELLOW button is pressed
        if power_down_pin.value() == 0:
            print("Power down is plugged in.")
        elif power_up_pin.value() == 0:
            print("Power up is plugged in.")
        else:
            print("No power port is connected.")
        if pilot_pin.value() == 1:
            print("Power signal to PILOT.")
        elif science_pin.value() == 1:
            print("Power signal to SCIENCE.")
        elif weapon_pin.value() == 1:
            print("Power signal to WEAPONS.")
        else:
            print("No power signal to any subsystems.")
        utime.sleep(0.2)  # Debounce delay to prevent multiple readings
    utime.sleep(0.1)