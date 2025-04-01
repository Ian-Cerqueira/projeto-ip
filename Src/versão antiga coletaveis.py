import pygame
from random import randint
from sys import exit

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Moeda(pygame.sprite.Sprite):
    def __init__(self, nome):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = randint(50, 450)
        self.rect.y = randint(50, 320)
        self.nome = nome
    #fazer uma def draw

class Chave(pygame.sprite.Sprite):
    def __init__(self, nome):
        super().__init__()
        self.image = pygame.Surface((40, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = screen_height // 2
        self.rect.y = screen_width - 240
        self.nome = nome

    #fazer uma def draw

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2
        self.rect.y = screen_height - 60
        self.velocidade = 5
        self.inventario = {'moeda': 0, 'chave': 0, 'estrela': 0}

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocidade

        # Mantém o jogador dentro da tela
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

    def add_moeda(self):
        self.inventario['moeda'] += 1

player1 = Player()

# Criar grupo de coletáveis
coletaveis = pygame.sprite.Group()
for item in range(10):
    coletaveis.add(Moeda(f'moeda'))

while True:
    screen.fill('Black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    player1.update(keys)

    # Verificar colisões e remover os coletáveis coletados
    coletados = pygame.sprite.spritecollide(player1, coletaveis, True)
    for coletado in coletados:
        print(f'Coletou {coletado.nome}')
        player1.add_moeda()
        print(player1.inventario)
    
    coletaveis.draw(screen)

    screen.blit(player1.image, player1.rect)

    pygame.display.update()
    clock.tick(60)
