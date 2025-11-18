from PiicoDev_Potentiometer import PiicoDev_Potentiometer
from PiicoDev_Unified import sleep_ms
 
from machine import Pin
import utime
import rp2

NUM_LEDS = 13
PIN_NUM = 22
brightness = 0.5

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
# Define the GPIO pin the button is connected to
button_pin = Pin(15, Pin.IN, Pin.PULL_DOWN)

pilot_pin = Pin(16, Pin.IN, Pin.PULL_DOWN)
science_pin = Pin(17, Pin.IN, Pin.PULL_DOWN)
weapon_pin = Pin(18, Pin.IN, Pin.PULL_DOWN)

power_down_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)
power_up_pin = Pin(1, Pin.IN, Pin.PULL_DOWN)
 
pot = PiicoDev_Potentiometer() # Initialise the potentiometer
pot.maximum = 100 # set the range of output values
pot.minimum = 0   # if minimum or maximum are ommitted, they will default to 0 and 100 respectively

last_slider = 0

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
        utime.sleep(0.2)
    if abs(last_slider - pot.value) > 1:
        last_slider = pot.value
        print(pot.value) # read the pot and print the result
    sleep_ms(100)