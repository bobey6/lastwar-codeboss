import pyautogui
import time
import threading

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

# The rest of your steps
steps = [first_step, "step2.png", "step3.png"]
confidence = 0.82
timeout_per_image = 30  # seconds
wait_between_loops = 30  # seconds

def wait_and_click(image, confidence, timeout):
    start_time = time.time()
    while True:
        try:
            location = pyautogui.locateCenterOnScreen(image, confidence=confidence)
            if location:
                pyautogui.moveTo(location)
                pyautogui.click()
                print(f"Clicked on {image}")
                return True
        except pyautogui.ImageNotFoundException:
            pass
        if time.time() - start_time > timeout:
            print(f"Timeout waiting for {image}, restarting sequence.")
            return False
        time.sleep(1)

def always_click_dmg_record():
    while True:
        try:
            location = pyautogui.locateCenterOnScreen("dmg_record.png", confidence=confidence)
            if location:
                pyautogui.moveTo(location)
                pyautogui.click()
                print("Clicked on dmg_record.png")
                time.sleep(1)  # Prevent rapid double clicks
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(0.5)

# Start the background thread
threading.Thread(target=always_click_dmg_record, daemon=True).start()

while True:
    print("Starting script...")
    for image in steps:
        found_and_clicked = wait_and_click(image, confidence, timeout_per_image)
        if not found_and_clicked:
            break  # Restart the sequence if a step times out
    print(f"Waiting {wait_between_loops} seconds before restarting...")
    time.sleep(wait_between_loops)