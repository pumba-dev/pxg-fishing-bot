import cv2
import numpy as np
import pytesseract
from PIL import ImageGrab

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

    return vida

# Chamada da função para obter a vida da tela
while True:
    vida = extractPokemonLife()
    print("Vida extraída:", vida)
