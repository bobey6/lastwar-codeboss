import pyautogui
import time
import threading
import sys

# Available first-step options
first_options = ["tank.png", "missle.png", "air.png"]

# Prompt the user at startup
print("Which image should be the first step?")
for i, img in enumerate(first_options, 1):
    print(f"{i}. {img}")
while True:
    try:
        choice = int(input("Enter the number of your choice: "))
        if 1 <= choice <= len(first_options):
            first_step = first_options[choice - 1]
            break
        else:
            print(f"Please enter a number between 1 and {len(first_options)}.")
    except ValueError:
        print("Please enter a valid number.")

# Sequence of steps
steps = [first_step, "step2.png", "step3.png"]
confidence = 0.82
timeout_per_image = 30  # seconds
wait_between_loops = 30  # seconds


def safe_locate_center(image, confidence):
    """Locate image on screen, return None if not found."""
    try:
        return pyautogui.locateCenterOnScreen(image, confidence=confidence)
    except pyautogui.ImageNotFoundException:
        return None


def wait_and_click(image, confidence, timeout):
    """Wait for an image to appear, then click it. Returns True if clicked, False on timeout."""
    start_time = time.time()
    while True:
        location = safe_locate_center(image, confidence)
        if location:
            pyautogui.moveTo(location)
            pyautogui.click()
            print(f"Clicked on {image}")
            return True
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for {image}, restarting sequence.")
            return False
        time.sleep(1)


def always_click_dmg_record():
    """Continuously look for dmg_record.png and click it if found."""
    while True:
        location = safe_locate_center("dmg_record.png", confidence)
        if location:
            pyautogui.moveTo(location)
            pyautogui.click()
            print("Clicked on dmg_record.png")
            time.sleep(1)  # Prevent rapid double clicks
        time.sleep(0.5)


def check_war_fever(confidence, timeout=15):
    """Look for war_fever.png before each run. Exit if not found within the timeout."""
    start_time = time.time()
    while True:
        location = safe_locate_center("war_fever.png", confidence)
        if location:
            print("Found war_fever.png, continuing...")
            return True
        if time.time() - start_time > timeout:
            print("Scout a base for War Fever before continuing")
            sys.exit(1)
        time.sleep(1)


# Start the background thread for dmg_record clicking
threading.Thread(target=always_click_dmg_record, daemon=True).start()

# Main loop
while True:
    # ✅ Pre-run check
    check_war_fever(confidence)

    print("Starting script...")
    for image in steps:
        found_and_clicked = wait_and_click(image, confidence, timeout_per_image)
        if not found_and_clicked:
            break  # Restart the sequence if a step times out
    print(f"Waiting {wait_between_loops} seconds before restarting...")
    time.sleep(wait_between_loops)
