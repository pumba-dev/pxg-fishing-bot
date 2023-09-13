import pyautogui
import myKeyboard

while True:
    bar = pyautogui.locateOnScreen("assets/general/minigameBar.jpg", confidence=0.75)
    fish = pyautogui.locateOnScreen("assets/general/minigameFish.jpg", confidence=0.75, grayscale=True)
    
    print('Bar: ' + str(bar) + ' - Fish: ' + str(fish))

    if bar != None and fish != None:
        if fish.top < bar.top:
            print('Pressing Space...')
            myKeyboard.key_down(0x39)
        else:
            myKeyboard.release_key(0x39)
    else:
        myKeyboard.key_down(0x39)
        myKeyboard.release_key(0x39)                