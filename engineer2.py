from PiicoDev_Potentiometer import PiicoDev_Potentiometer
from PiicoDev_Unified import sleep_ms
 
from machine import Pin
import utime
import rp2
import array, time
import random
import math

NUM_LEDS = 13
PIN_NUM = 22
brightness = 0.2
gauge = 0 
correct_gauge = 7
signal = ""


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

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)

def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
    
def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)

def gauge(level):
    color = GREEN
    if level >= 1 and level <= 4:
        color = RED
    elif level >= 4 and level <= 5:
        color = ORANGE
    elif level >= 6 and level <= 8:
        color = GREEN
    elif level >= 9 and level <= 10:
        color = ORANGE
    elif level >= 11 and level <= 13:
        color = RED
    for i in range(13):
        pixels_set(i, color)
    return color
    

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 117, 24)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)


#if correct_gauge != 7:
    #pass 
gauge(8)
pixels_show()

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
#print(pot.value) 

def slider_game(pot, WHITE):
    pixels_show()
    sweetspot = math.ceil(random.randint(0,100))
    color = WHITE
    level = 3
    while color != GREEN:
        if pot.value <= (sweetspot-20) or pot.value >= (sweetspot+20):
            level = 13
        elif pot.value <= (sweetspot-10) or pot.value >= (sweetspot+10):
            level = 10
        else:
            level = 7
        color = gauge(level)
        pixels_show()
        time.sleep(2)
    print("sweetspot reached!")

        
        
slider_game(pot, WHITE)


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
        if power_down_pin.value() == 0 and pilot_pin.value() == 1:
            print("R")
        elif power_down_pin.value() == 0 and science_pin.value() == 1:
            print("Y")
        elif power_down_pin.value() == 0 and weapon_pin.value() == 1:
            print("T")
        elif power_up_pin.value() == 0 and  pilot_pin.value() == 1:
            print('Q')
        elif power_up_pin.value() == 0 and weapon_pin.value() == 1:
            print('W')
        elif power_up_pin.value() == 0 and science_pin.value() == 1:
            print('E')
        utime.sleep(0.2)
    sleep_ms(100)
    signal = ""
    
