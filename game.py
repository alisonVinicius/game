import pgzrun
import math
import random
from pgzero.actor import Actor
from pgzero.builtins import keyboard




class Enemy(Actor):
    def __init__ (self, pos):
        super().__init__('enemy', pos)
        self.originalPos = pos
        self.speed = 0.2

    def resetPos(self):
        self.x = self.originalPos[0]
        self.y = self.originalPos[1]




class Axe(Actor):
    def __init__(self, owner, radius):
        super().__init__('axe', owner.pos)
        self.owner = owner  # O ator que "lançou" o machado (o lenhador)
        self.radius = radius # Distância do machado em relação ao centro do lenhador
        self.angle = 0 # Ângulo inicial de rotação
        self.rotation_speed = 5 # Velocidade de rotação
    
    def update(self):
        # Atualiza o ângulo
        self.angle += self.rotation_speed
        
        # Calcula a nova posição X e Y usando trigonometria
        # O centro de rotação é a posição do lenhador (self.owner.pos)
        self.x = self.owner.x + self.radius * math.cos(math.radians(self.angle))
        self.y = self.owner.y + self.radius * math.sin(math.radians(self.angle))




class Lumberjack(Actor):

    def __init__ (self, pos, speed):
        super().__init__('lumberjack', pos)
        self.life = 3
        self.speed = speed
        self.attack_timer = 50
        self.is_attacking = False
        self.axe = False


    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            # Cria uma instância da classe Axe
            self.axe = Axe(self, 50) # O '50' é o raio da rotação
            self.axe.draw()


    def update(self):
        # Lógica de Movimento
        if keyboard.left:
            self.x -= self.speed
        if keyboard.right:
            self.x += self.speed
        if keyboard.up:
            self.y -= self.speed
        if keyboard.down:
            self.y += self.speed

        # Lógica de Ataque
        if keyboard.z:
            self.attack()

            # Gerenciamento do Ataque (temporizador e atualização do machado)
            if self.is_attacking:
                if self.axe:
                    self.axe.update()

                if self.attack_timer <= 0:
                    self.is_attacking = False
                    self.axe = None
                    self.attack_timer = 200


    def lostLife(self):
        self.life -= 1
        if self.life < 0:
            self.life = 0
    
    def gainLife(self):
        self.life += 1
        if self.life > 3:
            self.life = 3


class Grass(Actor):
    def __init__(self, pos=(0, 0)):
        super().__init__('grass', pos)
        self.width = 16
        self.height = 16
        

class Tree(Actor):
    def __init__(self, pos=(0, 0)):
        super().__init__('tree', pos)

    def draw(self):
        Actor.draw(self)  



class Coin(Actor):
    def __init__(self, pos=(0, 0)):
        super().__init__('coin', pos)
        self.collected = False

    def draw(self):
        if not self.collected:
            Actor.draw(self)
        


# Initial Configuration
WIDTH      = 800      # Tamanho da janela do jogo
HEIGHT     = 600       # Tamanho da janela do jogo
MOVIMENT   = 1         # Velocidade inicial do lenhador
COIN_TIMER = 1000      # Tempo inicial que a moeda fica na tela (em frames)
sound_on   = True      # Variável para controlar o som
enemy_speed = 0.2    # Velocidade do inimigo



# Game Objects
# O mapa será constituido de gramas.
# o tamanho de cada imagem de cada tile é
#  tile  16px × 16px
# e o espaço entre as tiles é de
# Space  1px × 1px




# Lenhador
lumberjack = Lumberjack((WIDTH // 2, HEIGHT // 2), MOVIMENT)


# gramas
grass = Grass()

# moeda
coin = Coin()





tree_positions = []
trees = []
coin_positions = []
enemy = []

while len(tree_positions) < int( ((WIDTH + HEIGHT)//2) * 0.12):
    position = (random.randint(16, WIDTH), random.randint(32, HEIGHT - 16))
    
    # se a posição gerada não estiver na lista, adiciona
    if position not in tree_positions and position != (WIDTH  // 2, HEIGHT// 2):
        
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
            trees.append(Tree(position))

while len(coin_positions) < 200:
    position = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    
    # se a posição gerada não estiver na lista de árvores e nem na lista de moedas, adiciona
    if position not in tree_positions and position not in coin_positions:
    
        coin_positions.append(position)
    

while len(enemy) < 20:
    position = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
    
    # se a posição gerada não estiver na lista de árvores e nem na lista de moedas, adiciona
    if position not in tree_positions and position not in coin_positions:
        enemy.append(Enemy(position))
        



# Variáveis globais para moeda e contador
coin_timer = COIN_TIMER
fix_position_coin = random.randint(0, len(coin_positions) - 1)
coins_collected = 0
coin.pos = random.choice(coin_positions)


menu_active = True
menu_items = [
    {"text": "Começar Jogo", "action": "start_game"},
    {"text": "Música e sons : On", "action": "option_sound"},
    {"text": "Sair", "action": "exit_game"}]
selected_menu = 0


def draw_game():
    
        # Desenha o mesmo ator muitas vezes para preencher o fundo
        # Mais simples para preencher o fundo do que criar um  ator
        # para cada posição. Também funciona pelo fato da grama 
        # ser somente o fundo do jogo.
        for x in range(0, WIDTH, grass.width):
            for y in range(0, HEIGHT, grass.height):
                grass.topleft = (x, y)
                grass.draw()

        # desenha árvores em posições aleatórias
        # Aqui é necessário desenhar cada árvore individualmente
        # pois elas podem estar em posições diferentes
        for tree in trees:
            tree.draw()


        # desenha o lenhador
        lumberjack.draw()

        if lumberjack.axe:
            lumberjack.axe.draw()


        # desenha a moeda
        coin.draw()

        # desenha o inimigo
        for en in enemy:
            en.draw()


        # Desenha o contador de moedas
        screen.draw.text(f"Moedas: {coins_collected}", (10, 10), color="yellow", fontsize=20)
        screen.draw.text(f"velocidade: {lumberjack.speed:.2f}", (10, 30), color="yellow", fontsize=20)
        screen.draw.text(f"timer coin: {coin_timer}", (10, 50), color="yellow", fontsize=20)
        


def draw():

    global menu_active
    if menu_active:
        screen.fill((0, 128, 0))
        screen.draw.text("Lumberjack Game", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white")
        for idx, item in enumerate(menu_items):
            coler = "red" if idx == selected_menu else "white" # muda a cor do item selecionado
            text = item["text"]
            if item["action"] == "option_sound":
                if sound_on:
                    text = "Música e sons : On"
                else:
                    text = "Música e sons : Off"


            screen.draw.text(item["text"], center=(WIDTH // 2, HEIGHT // 2 + idx * 40), fontsize=40, color=coler)
    else:
       draw_game()
        

def update():
    global menu_active
    if not menu_active:
        update_game()


def update_game():



    # define a movimentação do lenhador

    # Salva a posição original
    original_x = lumberjack.x
    original_y = lumberjack.y


    # Movimentação do lenhador
    lumberjack.update()

    # Movimentação do inimigo (Vai atrás do lenhador)
    for en in enemy:



        # Desvia inimigos das árvores
        for tree in trees:
            if en.colliderect(tree):
                if en.x < tree.x:
                    en.x -= en.speed
                elif en.x > tree.x:
                    en.x += en.speed
                if en.y < tree.y:
                    en.y -= en.speed
                elif en.y > tree.y:
                    en.y += en.speed

        # Desvia inimigos entre si
        for other_en in enemy:
            if en != other_en and en.colliderect(other_en):
                if en.x < other_en.x:
                    en.x -= en.speed
                elif en.x > other_en.x:
                    en.x += en.speed
                if en.y < other_en.y:
                    en.y -= en.speed
                elif en.y > other_en.y:
                    en.y += en.speed

        # direcionando o inimigo para o lenhador
        if en.x < lumberjack.x:
            en.x += en.speed
        elif en.x > lumberjack.x:
            en.x -= en.speed
        if en.y < lumberjack.y:
            en.y += en.speed
        elif en.y > lumberjack.y:
            en.y -= en.speed


        # Colisão com o lenhador
        if lumberjack.colliderect(en):
            lumberjack.lostLife()
            lumberjack.pos = (WIDTH // 2, HEIGHT //2 )
            lumberjack.speed -= 0.01 
            en.speed += 0.01
            en.pos = en.originalPos

        if lumberjack.axe:
            if lumberjack.axe.colliderect(en):
                 en.speed += 0.001
                 en.pos = en.originalPos


        



    # Checa colisão com árvores
    for tree in trees:
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


    global  coin_timer, fix_position_coin, coins_collected, COIN_TIMER
    # decrementa o timer da moeda
    if coin_timer > 0:
        coin_timer -= 1
    else:
        coin_timer = COIN_TIMER
        fix_position_coin = random.randint(0, len(coin_positions) - 1)
        coin.collected = False
        coin.pos = coin_positions[fix_position_coin]

    # Checa colisão com a moeda
    if coin_timer > 0 and not coin.collected and lumberjack.colliderect(coin):
        coins_collected += 1
        coin.collected = True
        lumberjack.speed += 0.2
        coin_timer = 0
        COIN_TIMER -= 5
        if COIN_TIMER < 200:
            COIN_TIMER = 200
        coin.pos = (-100, -100)  # Move a moeda para fora da tela se coletada
        coin.pos = random.choice(coin_positions)


def on_key_down(key):
    global selected_menu, menu_active, sound_on
    if menu_active:
        if key == keys.UP:
            selected_menu = (selected_menu - 1) % len(menu_items)
        elif key == keys.DOWN:
            selected_menu = (selected_menu + 1) % len(menu_items)
        elif key == keys.RETURN or key == keys.SPACE:
            action = menu_items[selected_menu]["action"]
            if action == "start_game":
                menu_active = False
            elif action == "exit_game":
                quit()
            elif action == "option_sound":
                if sound_on:
                    sound_on = False

                else:
                    sound_on = True



    if keyboard.escape:
        menu_active = True
        return





pgzrun.go()

