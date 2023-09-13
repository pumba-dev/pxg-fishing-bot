# apertar o botão a cada 1 seg
import myKeyboard
from time import sleep

print("Press Ctrl-C to quit.")

def keyPress():
    myKeyboard.key_down(0x39)
    sleep(1)
    myKeyboard.release_key(0x39)

try:
    while True:
        keyPress()
        sleep(1)
except KeyboardInterrupt:
    print("\nDone.")
 