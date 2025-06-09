import lgpio
import time

# BCM GPIO pin numbers for rows and columns
ROWS = [16, 6, 13, 19]
COLS = [26, 20, 21]

KEY_MAP = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

def setup_pins(h):
    # Set rows as outputs, columns as inputs with pull-downs
    for row in ROWS:
        lgpio.gpio_claim_output(h, row, 0)
    for col in COLS:
        lgpio.gpio_claim_input(h, col, lgpio.SET_PULL_DOWN)

def getKey(h):
    while True:
        for i, row in enumerate(ROWS):
            # Set current row high, others low
            for r in ROWS:
                lgpio.gpio_write(h, r, 1 if r == row else 0)
            time.sleep(0.01)
            for j, col in enumerate(COLS):
                if lgpio.gpio_read(h, col):
                    # Debounce
                    time.sleep(0.1)
                    if lgpio.gpio_read(h, col):
                        key = KEY_MAP[i][j]
                        print(f'Key pressed: {key}')
                        # Wait for key release
                        while lgpio.gpio_read(h, col):
                            time.sleep(0.01)
                        return key

if __name__ == "__main__":
    h = lgpio.gpiochip_open(0)
    setup_pins(h)
    try:
        while True:
            KeyLucky = getKey(h)
            print(KeyLucky)
    except KeyboardInterrupt:
        pass
    finally:
        lgpio.gpiochip_close(h)