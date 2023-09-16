import pyautogui
from time import sleep
import myKeyboard
POKE_IMAGE_REGION=((50, 75, 0, 0))

def clickOnScreen(SQM, clickType = 'left'):
    position_x, position_y = pyautogui.center(SQM)
    pyautogui.moveTo(position_x, position_y, 0.1)
    if clickType == 'left':
        pyautogui.click()
    else:
        pyautogui.rightClick()
    sleep(0.1)

while True:
    sleep(1)

    print('Use revive in battle...')
    revive = None
    while revive == None:
            revive = pyautogui.locateOnScreen("assets/potions/revive_potion.jpg", region=(1692, 0, 214, 1080), confidence=0.9)
            if revive == None:
                print('Revive potion not detected...')
    clickOnScreen(POKE_IMAGE_REGION)
    clickOnScreen(revive, 'right')
    clickOnScreen(POKE_IMAGE_REGION)
    clickOnScreen(POKE_IMAGE_REGION)