from time import sleep
import pyautogui
import myKeyboard
import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab

RESTING_TIME=10
LOOT_KEY="F12"
FOOD_KEY="F11"
POKEBALL_KEY="NUMLOCK"
REVIVE_KEY="CAPS"
FISHING_ROD_KEY="Z"
MY_CHAR_REGION=(760, 361, 126, 104)
POTION_THRASHOLD=1750
POTION_TYPE="ultra"

attackList = ['shellder', 'tentacool', 'staryu', 'krabby']
# attackList = ['spheal', 'seel', 'chinchou']
catchList = ['shiny_tentacool', 'shiny_krabby', 'seel']
skillList = ["F5", "F4", "F3", "F1", "F2", "F6"]

def clickOnScreen(SQM, clickType = 'left'):
    position_x, position_y = pyautogui.center(SQM)
    pyautogui.moveTo(position_x, position_y, 0.5)
    if clickType == 'left':
        pyautogui.click()
    else:
        pyautogui.rightClick()
    sleep(0.3)

def catchPokemonsOnScreen():
    hasPokemon = True
    while hasPokemon:
        wasUsePokeball = False
        for name in catchList:
            pokemon = pyautogui.locateOnScreen(f"assets/catch/{name}_corpse.jpg", confidence=0.93)
            if pokemon != None:
                pokebola(pokemon, name)
                wasUsePokeball = True
                break
        if not wasUsePokeball:
            print("No Pokemons To Catch on Screen..")
            hasPokemon = False

def pokebola(corpseSQM, pokeName = '-'):
    print('Use pokeball on pokemon corpse: ', pokeName)
    myKeyboard.press(POKEBALL_KEY)
    sleep(0.5)
    clickOnScreen(corpseSQM)

while True:
    myKeyboard.press(POKEBALL_KEY)