import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# pin definitions so that they can be easily changed according to the schematic
BUTTON_PIN = 26


# 7-segment display pins
SEGMENT_PINS = [12, 4, 18, 23, 24, 27, 22]
# a, b, c, d, e, f, g this corresponds to the locations on the display

# this just initializes the pins in a for loop
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in [TL1_R, TL1_G, TL1_B, TL2_R, TL2_G, TL2_B] + SEGMENT_PINS:
    GPIO.setup(pin, GPIO.OUT)

# 7-segment display patterns
# this is just an array that makes it easier to transsalte gpio pins to real numbers also localizes them in case I make a mistake
SEGMENT_PATTERNS = {
    0: (1,1,1,1,1,1,0),
    1: (0,1,1,0,0,0,0),
    2: (1,1,0,1,1,0,1),
    3: (1,1,1,1,0,0,1),
    4: (0,1,1,0,0,1,1),
    5: (1,0,1,1,0,1,1),
    6: (1,0,1,1,1,1,1),
    7: (1,1,1,0,0,0,0),
    8: (1,1,1,1,1,1,1),
    9: (1,1,1,1,0,1,1)
}

# initialize to 0
last_press = 0

# this looks a little confusing but it just condenses a bunch of if statements and sets the color of the lights
def set_traffic_light(light, color):
    if light == 1:
        GPIO.output(TL1_R, color == 'red')
        GPIO.output(TL1_G, color == 'green')
        GPIO.output(TL1_B, color == 'blue')
    elif light == 2:
        GPIO.output(TL2_R, color == 'red')
        GPIO.output(TL2_G, color == 'green')
        GPIO.output(TL2_B, color == 'blue')

# uses zip and a for loop to combine the pin array with the pins that are supposed to be on
def display_number(number):
    for pin, value in zip(SEGMENT_PINS, SEGMENT_PATTERNS[number]):
        GPIO.output(pin, value)

# blinks light
def blink_light(light, color, times):
    for _ in range(times):
        set_traffic_light(light, color)
        time.sleep(0.5)
        set_traffic_light(light, 'off')
        time.sleep(0.5)

# main function
def traffic_light_sequence():
    # traffic light 2 turns blue, blinks 3 times, then turns red
    blink_light(2, 'blue', 3)
    set_traffic_light(2, 'red')
    
    # traffic light 1 turns green
    set_traffic_light(1, 'green')
    
    # for loop from 9 to -1 non inclusive with steps of -1
    for i in range(9, -1, -1):
        display_number(i)
        if i <= 4:
            blink_light(1, 'blue', 1)
        else:
            time.sleep(1)
    
    # traffic light 1 turns red
    # traffic light 2 turns green
    set_traffic_light(1, 'red')
    set_traffic_light(2, 'green')

# this just makes sure that the button can only be pressed every 20 seconds, its weird structurre just makes it resistant to any errors that might come on startup
def button_callback(channel):
    global last_press
    current_time = time.time()
    if current_time - last_press >= 20:
        last_press = current_time
        traffic_light_sequence()

# set up the interrupt
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

# initial
set_traffic_light(1, 'red')
set_traffic_light(2, 'green')

# just lets me know its running
print("traffic light system running interrupt method")

# allows the progrma to be stopped with keyboard input
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("program stopped")
    GPIO.cleanup()