import time
from gpiozero import LED, Button

# t1
r1 = LED(5)
g1 = LED(6)
b1 = LED(13)

# t2
r2 = LED(16)
g2 = LED(20)
b2 = LED(21)

# button
btn = Button(26)

# display
a = LED(17)
b = LED(4)
c = LED(18)
d = LED(23)
e = LED(24)
f = LED(27)
g = LED(22)

# display patterns
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

def display_number(number):
    segments = SEGMENT_PATTERNS[number]
    a.value, b.value, c.value, d.value, e.value, f.value, g.value = segments

def blink_light(light, times):
    for _ in range(times):
        light.on()
        time.sleep(0.5)
        light.off()
        time.sleep(0.5)

def traffic_light_sequence():
    b2.on()
    blink_light(b2, 3)
    r2.on()
    b2.off()
    
    g1.on()
    for i in range(9, -1, -1):
        display_number(i)
        if i <= 4:
            blink_light(b1, 1)
        else:
            time.sleep(1)
    g1.off()
    
    r1.on()
    r2.off()
    g2.on()

last_press_time = 0

def button_pressed():
    global last_press_time
    current_time = time.time()
    if current_time - last_press_time >= 20:
        last_press_time = current_time
        traffic_light_sequence()

btn.when_pressed = button_pressed

r1.on()
g2.on()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program stopped")