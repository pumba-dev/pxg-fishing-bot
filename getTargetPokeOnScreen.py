import cv2
import numpy as np
import pyautogui
import time

def encontrar_imagem_vermelha_na_tela():
    original_image = cv2.imread("assets/attack/magikarp_battle.jpg")
    
    # Converta a imagem original em preto e branco usando limiarização
    _, original_image_bw = cv2.threshold(original_image, 128, 255, cv2.THRESH_BINARY)

    # Salve a imagem em preto e branco para uso posterior, se necessário
    cv2.imwrite("assets/temp/current_attack_poke_binary.jpg", original_image_bw)

    # Carregue a imagem de destino (você pode precisar ajustar o caminho)
    imagem_alvo = cv2.imread("assets/temp/current_attack_poke_binary.jpg")

    # Capture a tela como uma imagem RGB
    tela = pyautogui.screenshot()
    imagem_tela = np.array(tela)
    imagem_tela_rgb = cv2.cvtColor(imagem_tela, cv2.COLOR_BGR2RGB)

    # Defina os limites inferior e superior para a cor vermelha no espaço RGB
    limite_inferior = np.array([0, 0, 100])
    limite_superior = np.array([100, 100, 255])

    # Crie uma máscara que identifica os pixels vermelhos na imagem da tela
    mascara_vermelha = cv2.inRange(imagem_tela_rgb, limite_inferior, limite_superior)

    # Aplicar a máscara vermelha na imagem da tela
    imagem_tela_mascarada = cv2.bitwise_and(imagem_tela, imagem_tela, mask=mascara_vermelha)

    # Compare a região da imagem mascarada com a imagem de destino
    resultado = cv2.matchTemplate(imagem_tela_mascarada, imagem_alvo, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

    # Defina um limite de confiança (ajuste conforme necessário)
    limite_confianca = 0.35

    if max_val >= limite_confianca:
        # A imagem de destino vermelha foi encontrada na tela
        print("Imagem vermelha encontrada!")

        # Obtenha as coordenadas da região correspondente
        x, y = max_loc
        w, h = imagem_alvo.shape[1], imagem_alvo.shape[0]

        # Retorne um array com as coordenadas (x, y, w, h)
        return [x, y, w, h]
    else:
        # A imagem de destino vermelha não foi encontrada na tela
        return None

# Loop contínuo para procurar a imagem na tela
while True:
    coordenadas = encontrar_imagem_vermelha_na_tela()
    print(coordenadas)

    # Espera um tempo antes de procurar novamente (você pode ajustar o tempo)
    time.sleep(1)
