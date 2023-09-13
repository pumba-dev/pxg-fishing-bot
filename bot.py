from time import sleep
import pyautogui
import myKeyboard
import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab

LOOT_KEY="F12"
RESTING_TIME=10
POTION_THRASHOLD=2000
POTION_TYPE="ultra"
POKEBALL_TYPE="ultra"
FOOD_TYPE="pizza"
MY_POKE_NAME='farfetch'

botWormsCount = 0
shinyCatchCount = 0
pokeCatchCount = 0
totalBattleCount = 0
attackList = ['sealeo', 'poliwhirl', 'seadra','seaking', 'spheal', 'seel', 'chinchou', 'shellder', 'tentacool', 'staryu', 'krabby', 'magikarp']
catchList = ['sealeo', 'poliwhirl', 'seadra','seaking', 'shiny_seadra', 'shiny_tentacool', 'shiny_krabby']
skillList = ["F5", "F4", "F3", "F1", "F7", "F9", "F2", "F6"]

def charIsFishing():
    leftFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_left.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    rightFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_right.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    southFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_south.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    northFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_north.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    if leftFishing != None:
        return leftFishing
    elif rightFishing != None:
        return rightFishing
    elif southFishing != None:
        return southFishing
    elif northFishing != None:
        return northFishing
    else:
        return None

def getAttackingPokemonRegion(pokeName):
    original_image = cv2.imread(f"assets/attack/{pokeName}_battle.jpg")
    _, original_image_bw = cv2.threshold(original_image, 128, 255, cv2.THRESH_BINARY)
    cv2.imwrite("assets/temp/current_attack_poke_binary.jpg", original_image_bw)

    imagem_alvo = cv2.imread("assets/temp/current_attack_poke_binary.jpg")

    tela = pyautogui.screenshot(region=BPREGION)
    imagem_tela = np.array(tela)
    imagem_tela_rgb = cv2.cvtColor(imagem_tela, cv2.COLOR_BGR2RGB)

    limite_inferior = np.array([0, 0, 100])
    limite_superior = np.array([100, 100, 255])

    mascara_vermelha = cv2.inRange(imagem_tela_rgb, limite_inferior, limite_superior)

    imagem_tela_mascarada = cv2.bitwise_and(imagem_tela, imagem_tela, mask=mascara_vermelha)

    resultado = cv2.matchTemplate(imagem_tela_mascarada, imagem_alvo, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

    limite_confianca = 0.35

    if max_val >= limite_confianca:
        x, y = max_loc
        w, h = imagem_alvo.shape[1], imagem_alvo.shape[0]
        return [x, y, w, h]
    else:
        return None

def getMyPokeBattleRegion():
    return pyautogui.locateOnScreen(f"assets/attack/{MY_POKE_NAME}_battle.jpg", region=BPREGION, confidence=0.90)

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
    tela = ImageGrab.grab()

    imagem = cv2.cvtColor(np.array(tela), cv2.COLOR_RGB2BGR)

    roi_x, roi_y, roi_largura, roi_altura = 97, 65, 176, 32
    roi = imagem[roi_y:roi_y+roi_altura, roi_x:roi_x+roi_largura]

    largura_aumentada = 2 * roi_largura  # Aumentar a largura
    altura_aumentada = 2 * roi_altura  # Aumentar a altura
    roi_aumentada = cv2.resize(roi, (largura_aumentada, altura_aumentada))

    roi_cinza = cv2.cvtColor(roi_aumentada, cv2.COLOR_BGR2GRAY)

    _, thresholded = cv2.threshold(roi_cinza, 185, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 2), np.uint8)
    thresholded = cv2.dilate(thresholded, kernel, iterations=1)
    kernel = np.ones((1, 2), np.uint8)
    thresholded = cv2.erode(thresholded, kernel, iterations=1)

    vida = pytesseract.image_to_string(thresholded, config='--oem 3 --psm 6')
    vida = vida.split('/')[0]

    try:
        lifeNum = int(vida)
    except:
        lifeNum = 99999999

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
    # print('Check Revive...')
    deadPokeball = pyautogui.locateOnScreen("assets/general/pokeballOff.jpg", region=(0,0,400,400), confidence=0.98)
    while deadPokeball != None:
        print('Try Reviving your pokemon..')
        revive = None
        while revive == None:
            revive = pyautogui.locateOnScreen("assets/potions/revive_potion.jpg", region=BPREGION, confidence=0.9)
        clickOnScreen(revive, 'right')
        clickOnScreen(deadPokeball)
        clickOnScreen(deadPokeball) 
        deadPokeball = pyautogui.locateOnScreen("assets/general/pokeballOff.jpg", region=(0,0,400,400), confidence=0.98)
        return True
    if deadPokeball == None:
        # print('Your pokemon is alive...')
        return False
        
def useAllAtacks():
    for skill in skillList:
        myKeyboard.press(skill)

def getFish():
    print('Pull fishing rod and get fish')
    fishingRod = pyautogui.locateOnScreen("assets/general/fishingRod.jpg", confidence=0.75)
    if fishingRod != None:
        clickOnScreen(fishingRod)
        sleep(1) # Wait minigame to start
        solveMinigame()
    else:
        print('Fishing rod not detected...')

def startFishing():
    print('Start fishing...')
    global botWormsCount
    botWormsCount += 1

    waterSQM = None
    while waterSQM == None:
        waterSQM = pyautogui.locateOnScreen("assets/general/waterToFishSQM.jpg", region=getCenterScreenRegion(600), confidence=0.75)

    fishingRod = pyautogui.locateOnScreen("assets/general/fishingRod.jpg", confidence=0.75)
    if fishingRod != None:
        clickOnScreen(fishingRod)
        clickOnScreen(waterSQM)
    else:
        print('Fishing rod not detected...')

def lootAround():
    print('Looting around...')
    myKeyboard.press(LOOT_KEY)
    sleep(0.3)

def solveMinigame():
    def getFish():
        return pyautogui.locateOnScreen("assets/general/minigameFish.jpg", confidence=0.65, grayscale=True)
    def getGameBar():
        return pyautogui.locateOnScreen("assets/general/minigameBar.jpg", confidence=0.87)
    
    BACKSPACE_KEY=0x39
    fish = getFish()

    if fish != None:
        print('Detected minigame, try to solve...')

    while fish != None:
        bar = getGameBar()
        fish = getFish()

        if bar != None and fish != None:
            if fish.top < bar.top:
                myKeyboard.key_down(BACKSPACE_KEY)
            else:
                myKeyboard.release_key(BACKSPACE_KEY)
        else:       
            myKeyboard.key_down(BACKSPACE_KEY)
            myKeyboard.release_key(BACKSPACE_KEY)    

def checkAndPutPokemonInBattle():
    pokeInBattle = pyautogui.locateOnScreen(f"assets/attack/{MY_POKE_NAME}_battle.jpg", region=BPREGION, confidence=0.90)
    if pokeInBattle == None:
        if checkRevive():
            return
        print("Put pokemon in battle..")
        myKeyboard.key_down(0x1D)
        myKeyboard.press('F1')
        myKeyboard.release_key(0x1D)

def atackPokemon(pokeTargetSQM, pokeName = ''):
    print('Start attack wild pokemon: ', pokeName) 
    clickOnScreen(pokeTargetSQM)
    global totalBattleCount
    totalBattleCount += 1

    attacking = True
    while attacking:
        checkRevive()    
        attacking = getAttackingPokemonRegion(pokeName)
        if attacking != None:
            useAllAtacks()
        else:
            print('Wild pokemon is dead...')
            attacking = False

def attackPokemonsOnScreen():
    hasPokemon = True
    killOne = False
    while hasPokemon:
        wasAttacked = False
        for name in attackList:
            pokemon = pyautogui.locateOnScreen(f"assets/attack/{name}_battle.jpg", region=BPREGION, confidence=0.90)
            if pokemon != None:
                wasAttacked = True
                killOne = True
                checkAndPutPokemonInBattle()
                atackPokemon(pokemon, name)
                break            
        if not wasAttacked:
            hasPokemon = False

    if not killOne:
        print("No Pokemons To Attack..")
        
    return killOne

def pokebola(corpseSQM, pokeName = '-'):
    print('Use pokeball on pokemon corpse: ', pokeName)

    if(pokeName.startswith('shiny_')):
        global shinyCatchCount
        shinyCatchCount += 1
    else:
        global pokeCatchCount
        pokeCatchCount += 1

    pokebalItem = pyautogui.locateOnScreen(f"assets/pokeballs/{POKEBALL_TYPE}_ball.jpg", region=BPREGION, confidence=0.95)
    if pokebalItem != None:
        clickOnScreen(pokebalItem, 'right')
        clickOnScreen(corpseSQM)
    else:
        print("Pokeball not detected...")

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
    # print("Check Pokemon Happyness...")
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
        
def myPokeIsHungry():
    original_image = cv2.imread("assets/poke-status/hungry_status.jpg")
    _, original_image_bw = cv2.threshold(original_image, 128, 255, cv2.THRESH_BINARY)
    cv2.imwrite("assets/temp/current_poke_hungry_status.jpg", original_image_bw)

    imagem_alvo = cv2.imread("assets/temp/current_poke_hungry_status.jpg")

    tela = pyautogui.screenshot(region=(0, 0, 300, 300))
    imagem_tela = np.array(tela)
    imagem_tela_rgb = cv2.cvtColor(imagem_tela, cv2.COLOR_BGR2RGB)

    limite_inferior = np.array([0, 0, 100])
    limite_superior = np.array([100, 100, 255])

    mascara_vermelha = cv2.inRange(imagem_tela_rgb, limite_inferior, limite_superior)

    imagem_tela_mascarada = cv2.bitwise_and(imagem_tela, imagem_tela, mask=mascara_vermelha)

    resultado = cv2.matchTemplate(imagem_tela_mascarada, imagem_alvo, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

    limite_confianca = 0.35

    if max_val >= limite_confianca:
        x, y = max_loc
        w, h = imagem_alvo.shape[1], imagem_alvo.shape[0]
        return [x, y, w, h]
    else:
        return None

def checkAndGivePokeFood():
    # print('Check If Pokemon is Hungry...')
    myPokeSQM = getMyPokeBattleRegion()
    hungryStatus = myPokeIsHungry()
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
    # else:
    #     print("Your pokemon is not hungry...")

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
    # print('Check Pokemon Life...')
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

while True:
    bolhas = pyautogui.locateOnScreen("assets/general/bubbleSQM.jpg", region=getCenterScreenRegion(600), confidence=0.75)
    fishing = charIsFishing()

    if fishing == None:
        print('Fishing not detected...')
        startFishing()
        print("Wait fish to bite the hook...")

    if bolhas != None:
        print('Fishing bubbles detected...')
        checkAndPutPokemonInBattle()

        getFish()

        if(len(attackList) > 0):
            if attackPokemonsOnScreen():
                lootAround()
            if len(catchList) > 0:
                catchPokemonsOnScreen()

        print("Battle Finished...")

        
        checkPokeLife()
        checkPokeHappyness()
        checkAndGivePokeFood()

        print("Waiting pokemon rest time...")
        sleep(RESTING_TIME)

        print("################################################")
        print('CONTADOR DE ISCAS:', botWormsCount)
        print('TENTATIVA DE SHINY:', shinyCatchCount)
        print('TENTATIVA DE POKE:', pokeCatchCount)
        print('TOTAL POKES DERROTADOS:', totalBattleCount)
        print('CONTADOR DE SHINY:', shinyCatchCount)
        

