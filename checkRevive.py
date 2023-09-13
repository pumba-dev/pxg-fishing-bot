import pyautogui
from time import sleep
import myKeyboard

while True:
    sleep(1)

    deadPokeball = pyautogui.locateOnScreen("assets/general/pokeballOff.jpg", confidence=0.98)
    print(deadPokeball)
    # if deadPokeball != None:
    #     print('Reviving your pokemon')
    #     myKeyboard.press("CAPS")
    #     # click pokeball
    #     position_x, position_y = pyautogui.center(deadPokeball)
    #     pyautogui.moveTo(position_x, position_y, 0.5)
    #     pyautogui.click()
    #     sleep(0.25)
    #     # Use pokemon revived
    #     pyautogui.click()     