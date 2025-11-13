import time
from machine import Pin

switch = Pin(15, Pin.IN, Pin.PULL_UP)
count = 0

time.sleep(1)
print('Ready to switch!')

while True:
    print(switch.value())
    if switch.value() != 1:
          count = count + 1
          print('Switch closed ', count)
          time.sleep(4)
    time.sleep(1)