from time import sleep
import pyautogui
import myKeyboard
import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab

RESTING_TIME=10
MY_CHAR_REGION=(760, 361, 126, 104)
POTION_THRASHOLD=2000
POTION_TYPE="ultra"
POKEBALL_TYPE="ultra"
FOOD_TYPE="pizza"

# attackList = ['shellder', 'tentacool', 'staryu', 'krabby', ]
# attackList = ['spheal', 'seel', 'chinchou']
attackList = ['sealeo', 'poliwhirl', 'seadra','seaking', 'magikarp']
catchList = ['sealeo', 'poliwhirl', 'seadra','seaking', 'shiny_seadra']
skillList = ["F5", "F4", "F3", "F1", "F2", "F6"]

def getCenterScreenRegion(size):
    largura, altura = pyautogui.size()
    centro_x = largura // 2
    centro_y = altura // 2
    x = centro_x - size // 2
    y = centro_y - size // 2
    x2 = x + size
    y2 = y + size
    return (x, y, x2, y2)

def extractPokemonLife():
    # Tirar um screenshot da tela inteira
    tela = ImageGrab.grab()
    # Converter o screenshot para uma imagem OpenCV
    imagem = cv2.cvtColor(np.array(tela), cv2.COLOR_RGB2BGR)
    # Defina a região de interesse (ROI)
    roi_x, roi_y, roi_largura, roi_altura = 97, 65, 176, 32
    roi = imagem[roi_y:roi_y+roi_altura, roi_x:roi_x+roi_largura]
    # Aplicar pré-processamento na ROI
    roi_cinza = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(roi_cinza, 150, 255, cv2.THRESH_BINARY)
    # Aplicar OCR (Reconhecimento Óptico de Caracteres)
    vida = pytesseract.image_to_string(thresholded, config='--psm 6')
    # Filtrar apenas os números antes do caractere '/'
    vida = vida.split('/')[0]

    try:
        lifeNum = int(vida)
    except:
        lifeNum = 0 

    return lifeNum

def clickOnScreen(SQM, clickType = 'left'):
    position_x, position_y = pyautogui.center(SQM)
    pyautogui.moveTo(position_x, position_y, 0.1)
    if clickType == 'left':
        pyautogui.click()
    else:
        pyautogui.rightClick()
    sleep(0.1)

def checkRevive():
    deadPokeball = pyautogui.locateOnScreen("assets/general/pokeballOff.jpg", region=(0,0,600,600), confidence=0.98)
    while deadPokeball != None:
        print('Try Reviving your pokemon..')
        revive = None
        while revive == None:
            revive = pyautogui.locateOnScreen("assets/potions/revive_potion.jpg", region=BPREGION, confidence=0.9)
        clickOnScreen(revive, 'right')
        clickOnScreen(deadPokeball)
        clickOnScreen(deadPokeball) 
        deadPokeball = pyautogui.locateOnScreen("assets/general/pokeballOff.jpg", region=(0,0,600,600), confidence=0.98)

def atackPokemon(pokeTargetSQM, pokeName = ''):
    print('Start attack wild pokemon: ', pokeName)
    
    clickOnScreen(pokeTargetSQM)

    attacking = True
    while attacking:
        checkRevive()    
        attacking = pyautogui.locateOnScreen(f"assets/attack/{pokeName}_battle.jpg", region=BPREGION, confidence=0.9)
        if attacking != None:
            print('Attacking wild pokemon...')  
            useAllAtacks()
            changeTarget = pyautogui.locateOnScreen("assets/general/changeTarget.jpg", confidence=0.9)
            if changeTarget != None:
                attacking = False
                print('Wild pokemon is dead...')
        else:
            print('Wild pokemon is dead...')
            attacking = False

def useAllAtacks():
    for skill in skillList:
        myKeyboard.press(skill)

def getFish():
    print('Pull fishing rod and get fish')
    fishingRod = pyautogui.locateOnScreen("assets/general/fishingRod.jpg", confidence=0.75)
    if fishingRod != None:
        clickOnScreen(fishingRod)
        sleep(1)
        solveMinigame()

def startFishing():
    print('Start fishing...')
    fishingRod = pyautogui.locateOnScreen("assets/general/fishingRod.jpg", confidence=0.75)
    waterSQM = None
    while waterSQM == None:
        waterSQM = pyautogui.locateOnScreen("assets/general/waterToFishSQM.jpg", region=getCenterScreenRegion(600), confidence=0.75)

    if fishingRod != None:
        clickOnScreen(fishingRod)
        clickOnScreen(waterSQM)
    else:
        print('Fishing rod not detected...')

def lootAround():
    print('Looting around...')
    myKeyboard.press(LOOT_KEY)
    sleep(0.3)

def pokebola(corpseSQM, pokeName = '-'):
    print('Use pokeball on pokemon corpse: ', pokeName)
    pokebalItem = pyautogui.locateOnScreen(f"assets/pokeballs/{POKEBALL_TYPE}_ball.jpg", region=BPREGION, confidence=0.95)
    clickOnScreen(pokebalItem, 'right')
    clickOnScreen(corpseSQM)

def solveMinigame():
    fish = True
    while fish != None:
        bar = pyautogui.locateOnScreen("assets/general/minigameBar.jpg", confidence=0.87)
        fish = pyautogui.locateOnScreen("assets/general/minigameFish.jpg", confidence=0.65, grayscale=True)

        print('Trying to solve minigame...')
        if bar != None and fish != None:
            if fish.top < bar.top:
                myKeyboard.key_down(0x39)
            else:
                myKeyboard.release_key(0x39)
        else:       
            myKeyboard.key_down(0x39)
            myKeyboard.release_key(0x39)    

    print('Dont detected minigame...') 

def checkAndPutPokemonInBattle():
    pokeInBattle = pyautogui.locateOnScreen("assets/general/pokeInBattle.jpg", confidence=0.9)
    if pokeInBattle == None:
        print("Put pokemon in battle..")
        myKeyboard.key_down(0x1D)
        myKeyboard.press('F1')
        myKeyboard.release_key(0x1D)

def attackPokemonsOnScreen():
    hasPokemon = True
    while hasPokemon:
        wasAttacked = False
        for name in attackList:
            pokemon = pyautogui.locateOnScreen(f"assets/attack/{name}_battle.jpg", region=BPREGION, confidence=0.65, grayscale=True)
            if pokemon != None:
                wasAttacked = True
                checkAndPutPokemonInBattle()
                atackPokemon(pokemon, name)
                break            
        if not wasAttacked:
            print("No Pokemons to Attack..")
            hasPokemon = False

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
            print("No Pokemons To Catch..")
            hasPokemon = False

def checkPokeHappyness():
    print("Check Pokemon Happyness...")
    rageStatus = pyautogui.locateOnScreen("assets/poke-status/rage_status.jpg", confidence=0.9)
    badStatus = pyautogui.locateOnScreen("assets/poke-status/bad_status.jpg", confidence=0.9)
    sadStatus = pyautogui.locateOnScreen("assets/poke-status/sad_status.jpg", confidence=0.9)

    if rageStatus != None:
        print("Give love to pokemon...")
        clickOnScreen(rageStatus)
    elif badStatus != None:
        print("Give love to pokemon...")
        clickOnScreen(badStatus)
    elif sadStatus != None:
        print("Give love to pokemon...")
        clickOnScreen(sadStatus)
        
def checkPokeHungry():
    print('Check If Pokemon is Hungry...')
    myPokeSQM = pyautogui.locateOnScreen("assets/attack/mypoke_battle.jpg", confidence=0.98)
    hungryStatus = pyautogui.locateOnScreen("assets/poke-status/hungry_status.jpg", confidence=0.95)
    if hungryStatus != None:
        print("Give food to pokemon...")
        foodItem = pyautogui.locateOnScreen(f"assets/foods/{FOOD_TYPE}_food.jpg", confidence=0.95)
        if foodItem != None:
            clickOnScreen(foodItem, 'right')
            if myPokeSQM != None:
                clickOnScreen(myPokeSQM)
                sleep(0.3)
            else:
                print("Your pokemon not detected...")
        else:
            print("Food not detected...")
    else:
        print("Your pokemon is not hungry...")

def usePotionInPokemon(potion):
    print("Use potion in pokemon: " + potion)
    potionItem = pyautogui.locateOnScreen(f"assets/potions/{potion}_potion.jpg", region=BPREGION, confidence=0.9)
    if potionItem != None:
        clickOnScreen(potionItem, 'right')
        MyPokeBattle = pyautogui.locateOnScreen("assets/attack/mypoke_battle.jpg", confidence=0.98)
        if MyPokeBattle != None:
            clickOnScreen(MyPokeBattle)
        else:
            print("My pokemon not detected...")
    else:
        print("Potion not detected...")

def checkPokeLife():
    print('Check Pokemon Life...')
    life = extractPokemonLife()
    print("Pokemon Life:", life)
    if life <= POTION_THRASHOLD:
        usePotionInPokemon(POTION_TYPE)

def getBPArea():
    initialBPArea = pyautogui.locateOnScreen("assets/general/initialBPArea.jpg", confidence=0.9)
    endBPArea = pyautogui.locateOnScreen("assets/general/endBPArea.jpg", confidence=0.9)
    if initialBPArea != None and endBPArea != None:
        position_x, position_y = pyautogui.center(initialBPArea)
        position_x2, position_y2 = pyautogui.center(endBPArea)
        screenYSize = pyautogui.size()[1]
        
        bpArea = (position_x, 0, position_x2 - position_x, screenYSize)
        print("BP Area detected: ", bpArea)
        return bpArea
    else:
        print("BP Area not detected...")
        return None

print("################################################")
print("PXG Fishing Bot Started!!")
print("Please, start fishing on game.")
print("Press Ctrl-C to quit.")
print("################################################")

BPREGION = getBPArea()
sleep(0.25)
checkRevive()
sleep(0.25)
checkPokeLife()
sleep(0.25)
checkAndPutPokemonInBattle()
sleep(0.25)
attackPokemonsOnScreen()
sleep(0.25)
lootAround()
sleep(0.25)
catchPokemonsOnScreen()
sleep(0.25)

count = 1

while True:
    bolhas = pyautogui.locateOnScreen("assets/general/bubbleSQM.jpg", confidence=0.75)
    fishing = pyautogui.locateOnScreen("assets/general/fishingSkin.jpg", region=MY_CHAR_REGION, confidence=0.75)

    if fishing == None:
        print('Fishing not detected...')
        startFishing()

    if bolhas != None:
        print('Fishing bubbles detected...')
        print('ISCAS USADAS:', count)
        checkAndPutPokemonInBattle()

        getFish()

        attackPokemonsOnScreen()
        checkRevive()
        lootAround()
        if len(catchList) > 0:
            catchPokemonsOnScreen()

        checkPokeLife()

        print("Battle Finished...")

        checkRevive()
        sleep(RESTING_TIME)

        checkPokeHappyness()

        checkPokeHungry()

        count += 1

