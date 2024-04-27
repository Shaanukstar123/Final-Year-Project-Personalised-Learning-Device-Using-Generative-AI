import digitalio
import board
import time

reed = digitalio.DigitalInOut(board.D17)
reed.switch_to_input(pull=digitalio.Pull.UP)

while True:
        if reed.value:
                print("Open")
        else:
                print("Closed")
        time.sleep(0.2)