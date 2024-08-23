import RPi.GPIO as GPIO
import time

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin definitions
BUTTON_PIN = 26
TL1_R, TL1_G, TL1_B = 5, 6, 13  # Traffic Light 1 pins
TL2_R, TL2_G, TL2_B = 16, 20, 19  # Traffic Light 2 pins
SEGMENT_PINS = [12, 4, 18, 23, 24, 27, 22]  # a, b, c, d, e, f, g

# Setup pin modes
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
for pin in [TL1_R, TL1_G, TL1_B, TL2_R, TL2_G, TL2_B] + SEGMENT_PINS:
    GPIO.setup(pin, GPIO.OUT)

# 7-segment display patterns
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

last_press_time = 0

def set_traffic_light(light, color):
    if light == 1:
        GPIO.output(TL1_R, color == 'red')
        GPIO.output(TL1_G, color == 'green')
        GPIO.output(TL1_B, color == 'blue')
    elif light == 2:
        GPIO.output(TL2_R, color == 'red')
        GPIO.output(TL2_G, color == 'green')
        GPIO.output(TL2_B, color == 'blue')

def display_number(number):
    for pin, value in zip(SEGMENT_PINS, SEGMENT_PATTERNS[number]):
        GPIO.output(pin, value)

def blink_light(light, color, times):
    for _ in range(times):
        set_traffic_light(light, color)
        time.sleep(0.5)
        set_traffic_light(light, 'off')
        time.sleep(0.5)

def traffic_light_sequence():
    # Traffic light 2 turns blue, blinks 3 times, then turns red
    blink_light(2, 'blue', 3)
    set_traffic_light(2, 'red')
    
    # Traffic light 1 becomes green and countdown starts
    set_traffic_light(1, 'green')
    for i in range(9, -1, -1):
        display_number(i)
        if i <= 4:
            blink_light(1, 'blue', 1)
        else:
            time.sleep(1)
    
    # Traffic light 1 becomes red, traffic light 2 becomes green
    set_traffic_light(1, 'red')
    set_traffic_light(2, 'green')

def button_callback(channel):
    global last_press_time
    current_time = time.time()
    if current_time - last_press_time >= 20:
        last_press_time = current_time
        traffic_light_sequence()

# Initial state
set_traffic_light(1, 'red')
set_traffic_light(2, 'green')

print("Traffic light system running (Interrupt method). Press Ctrl+C to exit.")

try:
    # Remove any existing event detection on the button pin
    GPIO.remove_event_detect(BUTTON_PIN)
    
    # Set up the interrupt with error handling
    try:
        GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)
        print("Interrupt set up successfully")
    except Exception as e:
        print(f"Error setting up interrupt: {e}")
        GPIO.cleanup()
        exit(1)

    # Keep the program running
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped")
finally:
    GPIO.cleanup()