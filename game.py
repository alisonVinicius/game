
import pgzrun
import math
import random
from pgzero.actor import Actor
from pgzero.builtins import keyboard


# Initial Configuration
WIDTH = 1200
HEIGHT = 600
MOVIMENT = 1
COIN_TIMER = 1000
speed = MOVIMENT

# Game Objects
# O mapa será constituido de gramas.
# o tamanho de cada imagem de cada tile é
#  tile  16px × 16px
# e o espaço entre as tiles é de
# Space  1px × 1px

# Lenhador
lumberjack = Actor('lumberjack')

# posição inicial do lenhador é no centro da tela.
lumberjack.pos = (WIDTH // 2, HEIGHT // 2)

# gramas
grass = Actor('grass')

# arvores, cogumelos e moedas
tree = Actor('tree')
tree2 = Actor('tree2')
mushroom = Actor('mushroom')
coin = Actor('coin')


# define o tamanho de grass
grass.width = 16
grass.height = 16


tree_positions = []
coin_positions = []

while len(tree_positions) < ((WIDTH + HEIGHT)//2) * 0.12:
    position = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    
    # se a posição gerada não estiver na lista, adiciona
    if position not in tree_positions and position != (lumberjack.x, lumberjack.y):
        
        # para evitar choques entre árvores, verifica se as árvores ficam a pelo menos 16 pixels de distância
        too_close = False
        for pos in tree_positions:

            # Observe que usar hypot é mais preciso porque define a distância euclidiana
            # dos pontos calculados.
            if math.hypot(position[0] - pos[0], position[1] - pos[1]) < 32:
                too_close = True
                break
        
        if not too_close:
            tree_positions.append(position)

while len(coin_positions) < 20:
    position = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    
    # se a posição gerada não estiver na lista de árvores e nem na lista de moedas, adiciona
    if position not in tree_positions and position not in coin_positions:
    
        coin_positions.append(position)
    


# Variáveis globais para moeda e contador
coin_timer = COIN_TIMER
fix_position_coin = random.randint(0, len(coin_positions) - 1)
coins_collected = 0


def draw():
    # como o tamanho da tela é 1920x1080 e o tamanho de cada tile é 16x16
    # precisamos desenhar 120 tiles na horizontal e 67.5 na vertical
    for x in range(0, WIDTH, grass.width):
        for y in range(0, HEIGHT, grass.height):
            grass.topleft = (x, y)
            grass.draw()

    # desenha árvores em posições aleatórias
    for x in tree_positions:
        tree.pos = (x)
        tree2.pos = (x[0], x[1] - 16)
        tree2.draw()
        tree.draw()

    # desenha o lenhador
    lumberjack.draw()


    global coin_timer, coins_collected
    if coin_timer > 0:
        coin.pos = (coin_positions[fix_position_coin])
        coin.draw()

    # Desenha o contador de moedas
    screen.draw.text(f"Moedas: {coins_collected}", (10, 10), color="yellow", fontsize=20)
    screen.draw.text(f"velocidade: {speed:.2f}", (10, 30), color="yellow", fontsize=20)
    screen.draw.text(f"timer coin: {coin_timer}", (10, 50), color="yellow", fontsize=20)
    
    




def update():
    # define a movimentação do lenhador

    # Salva a posição original
    original_x = lumberjack.x
    original_y = lumberjack.y


    # Movimentação do lenhador
    global speed
    if keyboard.left:
        lumberjack.x -= speed
    if keyboard.right:
        lumberjack.x += speed
    if keyboard.up:
        lumberjack.y -= speed
    if keyboard.down:
        lumberjack.y += speed


    # Checa colisão com árvores
    for pos in tree_positions:
        tree.pos = pos
        if lumberjack.colliderect(tree):
            # Reverte o movimento
            lumberjack.x = original_x
            lumberjack.y = original_y
            break


    # limite da movimentação do lenhador
    if lumberjack.x < 0:
        lumberjack.x = 0
    if lumberjack.x > WIDTH:
        lumberjack.x = WIDTH
    if lumberjack.y < 0:
        lumberjack.y = 0
    if lumberjack.y > HEIGHT:
        lumberjack.y = HEIGHT


    global coin_timer, fix_position_coin, coins_collected, COIN_TIMER
    # decrementa o timer da moeda
    if coin_timer > 0:
        coin_timer -= 1
    else:
        coin_timer = COIN_TIMER
        fix_position_coin = random.randint(0, len(coin_positions) - 1)


    # Checa colisão com a moeda (só conta uma vez por moeda)
    if coin_timer > 0 and lumberjack.colliderect(coin):
        coins_collected += 1
        coin_timer = 0  # Faz a moeda desaparecer
        speed += 0.04  # Aumenta a velocidade do lenhador a cada moeda coletada
        COIN_TIMER -= 10 # Diminui o tempo da moeda a cada moeda coletada
        # Move a moeda para fora da tela para evitar múltiplas colisões no mesmo frame
        coin.pos = (-100, -100)


pgzrun.go()

