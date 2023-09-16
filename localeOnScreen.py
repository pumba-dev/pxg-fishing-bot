import pyautogui
from PIL import Image
import numpy as np
import time

# Loop contínuo para procurar a imagem na tela
while True:
    area = pyautogui.locateOnScreen("assets/general/lifeArea.jpg", region=(0,0,300,100), confidence=0.5, grayscale=True)
    print('Region: ', area)
    time.sleep(1)
