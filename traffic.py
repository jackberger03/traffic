from gpiozero import LED, Button
from signal import pause
import time

# Pin definitions
button = Button(26)
tl1_r, tl1_g, tl1_b = LED(5), LED(6), LED(13)  # Traffic Light 1
tl2_r, tl2_g, tl2_b = LED(16), LED(20), LED(19)  # Traffic Light 2
segments = [LED(pin) for pin in [12, 4, 18, 23, 24, 27, 22]]  # a, b, c, d, e, f, g

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
        tl1_r.value, tl1_g.value, tl1_b.value = color == 'red', color == 'green', color == 'blue'
    elif light == 2:
        tl2_r.value, tl2_g.value, tl2_b.value = color == 'red', color == 'green', color == 'blue'

def display_number(number):
    for segment, value in zip(segments, SEGMENT_PATTERNS[number]):
        segment.value = value

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

def button_pressed():
    global last_press_time
    current_time = time.time()
    if current_time - last_press_time >= 20:
        last_press_time = current_time
        traffic_light_sequence()

# Set up the button press event
button.when_pressed = button_pressed

# Initial state
set_traffic_light(1, 'red')
set_traffic_light(2, 'green')

print("Traffic light system running. Press Ctrl+C to exit.")

try:
    pause()  # Keep the script running
except KeyboardInterrupt:
    print("Program stopped")