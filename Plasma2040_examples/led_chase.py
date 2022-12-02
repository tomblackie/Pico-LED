import plasma
from plasma import plasma2040
import time
import random

# Import helpers for RGB LEDs, Buttons, and Analog
from pimoroni import RGBLED, Button, Analog

# Press "B" to speed up the LED cycling effect.
# Press "A" to slow it down again.
# Press "Boot" to reset the speed back to default.

# Set how many LEDs you have
NUM_LEDS = 144

# The speed that the LEDs will start cycling at
DEFAULT_SPEED = 100

# How many times the LEDs will be updated per second
UPDATES = 60


# Pick *one* LED type by uncommenting the relevant line below:

# APA102 / DotStar™ LEDs
# led_strip = plasma.APA102(NUM_LEDS, 0, 0, plasma2040.DAT, plasma2040.CLK)

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)

user_sw = Button(plasma2040.USER_SW)
button_a = Button(plasma2040.BUTTON_A)
button_b = Button(plasma2040.BUTTON_B)
led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)
sense = Analog(plasma2040.CURRENT_SENSE, plasma2040.ADC_GAIN, plasma2040.SHUNT_RESISTOR)

# Start updating the LED strip
led_strip.start()

# led_strip.set_brightness(3)

speed = DEFAULT_SPEED
offset = 0.0

count = 0

direction = 1


# Make rainbows
while True:
    sw = user_sw.read()
    a = button_a.read()
    b = button_b.read()

    if sw:
        speed = DEFAULT_SPEED
    else:
        if a:
            speed -= 1
        if b:
            speed += 1

    speed = min(255, max(1, speed))

    offset += float(speed) / 2000.0


    for i in range(NUM_LEDS):

        if direction == 1:
            led_strip.set_rgb(i, 128, 0, 0 )
            time.sleep(1 / speed)
            led_strip.set_rgb(i, 0, 0, 0)
        else:
            led_strip.set_rgb(NUM_LEDS - i, 0, 128, 0)
            time.sleep(1 / speed)
            led_strip.set_rgb(NUM_LEDS - i, 0, 0, 0)

        if i == NUM_LEDS - 1:
            direction *= -1
        
        # print(direction, i)
    print("Current =", sense.read_current(), "A")

    # led.set_rgb(speed, 0, 255 - speed)

    count += 1
    print("Cycle =", count)
    if count >= UPDATES:
        # Display the current value once every second
        print("Current =", sense.read_current(), "A")
        count = 0

    time.sleep(1.0 / UPDATES)
