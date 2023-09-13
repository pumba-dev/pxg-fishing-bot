import pyautogui
import myKeyboard

while True:
    pokeInBattle = pyautogui.locateOnScreen("assets/general/pokeInBattle.jpg", confidence=0.9)
    print(pokeInBattle)
    if pokeInBattle == None:
        print("Put pokemon in battle..")
        myKeyboard.key_down(0x1D)
        myKeyboard.press('F1')
        myKeyboard.release_key(0x1D)