import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab

def extractPokemonLife():
    tela = ImageGrab.grab()

    imagem = cv2.cvtColor(np.array(tela), cv2.COLOR_RGB2BGR)

    roi_x, roi_y, roi_largura, roi_altura = 0, 0, 100, 150
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

    cv2.imshow("Imagem em binário", thresholded)
    cv2.waitKey(0)

    vida = pytesseract.image_to_string(thresholded, config='--oem 3 --psm 6')
    print('Vida:', vida)
    vida = vida.split('/')[0]

    return vida

# Chamada da função para obter a vida da tela
while True:
    vida = extractPokemonLife()
    print("Vida extraída:", vida)
