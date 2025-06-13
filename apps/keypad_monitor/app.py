import keypad

def monitor_keypad():
    country_prefix = ""
    while True:
        if keypad.is_off_hook():
            if key := keypad.get_button():
                country_prefix += key
        else:
            country_prefix = ""


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
