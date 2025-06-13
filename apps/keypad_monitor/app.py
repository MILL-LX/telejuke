import keypad

def monitor_keypad():
    """
    Continuously monitors the keypad for key presses and prints the pressed keys.
    """
    print("Starting keypad monitor...")
    while True:
        key = keypad.get_button()
        if key is not None:
            print(f"Key pressed: {key}")
        else:
            print("No key pressed.")

if __name__ == "__main__":
    keypad.setup()  # Initialize the keypad hardware
    try:
        print("Keypad monitor is running. Press Ctrl+C to exit.")
        monitor_keypad()
    except KeyboardInterrupt:
        pass
    finally:
        keypad.cleanup()  # Cleanup GPIO pins if needed

    print("Keypad monitor stopped.")
