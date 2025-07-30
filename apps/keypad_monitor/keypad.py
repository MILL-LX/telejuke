import lgpio
import time

import dtmf

# BCM GPIO pin numbers for rows and columns
ROW_PINS = [16, 6, 13, 19]
COLUMN_PINS = [26, 20, 21]

KEY_MAP = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

# BCM GPIO pin for off hook switch
OFF_HOOK_PIN = 12

global h
def setup():
    global h
    h = lgpio.gpiochip_open(0)  # Open GPIO chip 0
    if h < 0:
        raise RuntimeError("Failed to open GPIO chip")
    
    # Set rows as outputs, columns as inputs with pull-downs
    for row in ROW_PINS:
        lgpio.gpio_claim_output(h, row, 0)
    for col in COLUMN_PINS:
        lgpio.gpio_claim_input(h, col, lgpio.SET_PULL_DOWN)

    # Set off hook pin as input with pull-up
    lgpio.gpio_claim_input(h, OFF_HOOK_PIN, lgpio.SET_PULL_UP)

    dtmf.init_digit_tones()

def cleanup():
    global h
    if h is not None:
        lgpio.gpiochip_close(h)
        h = None

def is_off_hook():
    off_hook = 1 == lgpio.gpio_read(h, OFF_HOOK_PIN)
    return off_hook

def get_button():
    while is_off_hook():
        for i, row in enumerate(ROW_PINS):
            # Set current row high, others low
            for r in ROW_PINS:
                lgpio.gpio_write(h, r, 1 if r == row else 0)
            time.sleep(0.01)
            for j, col in enumerate(COLUMN_PINS):
                if lgpio.gpio_read(h, col):
                    # Debounce
                    # time.sleep(0.01)
                    if lgpio.gpio_read(h, col):
                        button = KEY_MAP[i][j]
                        dtmf.play_digit(button)  # Play DTMF tone

                        while lgpio.gpio_read(h, col):
                            time.sleep(0.1)
                            
                        dtmf.stop_playing_digit()
                        return button
    return None