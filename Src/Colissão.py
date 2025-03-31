import pygame
from random import randint
from sys import exit

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
BLUE = (0, 0, 255)

class Coletavel:
    def __init__(self, nome):
        self.nome = nome
        self.valor = randint(10, 50)
        self.x = randint(50, 450)
        self.y = randint(50, 320)
        self.coletado = False
    
    def draw(self):
        if not self.coletado:  # Só desenha se não tiver sido coletado
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 40, 50))

    def update(self):
        self.coletado = True  # Marca como coletado

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2
        self.rect.y = screen_height - 60
        self.velocidade = 5
        self.inventario = {'moeda': 0}

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - self.rect.width:
            self.rect.x = screen_width - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height
    
    def add_moeda(self):
        self.inventario['moeda'] += 1

# Função para verificar a colisão entre o jogador e o coletável
def verificar_colisao(player, coleta):
    if player.rect.colliderect(pygame.Rect(coleta.x, coleta.y, 40, 50)):
        return True
    return False

player1 = Player()
coleta = Coletavel('Ian')

while True:
    screen.fill('Black')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    player1.update(keys)
    
    # Desenha o coletável (se não tiver sido coletado)
    coleta.draw()

    # Verifica a colisão e coleta o objeto
    if verificar_colisao(player1, coleta):
        print('Coletou')
        player1.add_moeda()
        print(player1.inventario)
        coleta.update()  # Marca o coletável como coletado

    # Desenha o jogador
    screen.blit(player1.image, player1.rect)
    
    pygame.display.update()
    clock.tick(60)
