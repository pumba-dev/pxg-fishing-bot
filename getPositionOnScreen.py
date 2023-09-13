# Obter posição do mouse na tela no próximo click com botão esquerdo.
import cv2
import numpy as np
import pyautogui

def detectAttack(image_path):
    original_image = cv2.imread(image_path)
    red_filter = np.zeros_like(original_image)
    red_filter[:,:,2] = original_image[:,:,2] 
    cv2.imwrite("assets/temp/current_attack_poke.jpg", red_filter)

    attacking = pyautogui.locateOnScreen("assets/temp/current_attack_poke.jpg", confidence=0.98, grayscale=True)
    return attacking

print("Press Ctrl-C to quit.")
try:
    while True:
        # attacking = detectAttack("assets/attack/magikarp_battle.jpg")
        image = pyautogui.locateOnScreen("assets/general/lifeArea.jpg", region=(0,0, 500, 500), confidence=0.6, grayscale=True)
        print(image)
        
except KeyboardInterrupt:
    print("\nDone.")

    