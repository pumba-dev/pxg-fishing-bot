import cv2
import numpy as np
import pyautogui
import time

def getCenterScreenRegion(size):
    largura, altura = pyautogui.size()
    centro_x = largura // 2
    centro_y = altura // 2
    x = centro_x - size // 2
    y = centro_y - size // 2
    x2 = x + size
    y2 = y + size
    return (x, y, x2, y2)

# Loop contínuo para procurar a imagem na tela
while True:
    leftFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_left.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    rightFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_right.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    southFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_south.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    northFishing = pyautogui.locateOnScreen("assets/char-skin/fishing_north.jpg", region=getCenterScreenRegion(400), confidence=0.9)
    
    print('leftFishing: ', leftFishing)
    print('rightFishing: ', rightFishing)
    print('southFishing: ', southFishing)
    print('northFishing: ', northFishing)


    # Espera um tempo antes de procurar novamente (você pode ajustar o tempo)
    time.sleep(1)
