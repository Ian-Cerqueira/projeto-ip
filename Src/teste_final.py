import pygame as pg
from coletaveis_01 import ItemColetavel
from foes import Foes
from player import Player
import sys

pg.init()

def criar_itens(qtd_moedas, qtd_chaves, qtd_estrelas):
    grupo = pg.sprite.Group()
    for _ in range(qtd_moedas): grupo.add(ItemColetavel('moeda', 170, 350))
    for _ in range(qtd_chaves): grupo.add(ItemColetavel('chave', 280, 350))
    for _ in range(qtd_estrelas): grupo.add(ItemColetavel('estrela', 400, 250))
    return grupo

coletaveis = criar_itens(qtd_moedas=1, qtd_chaves=1, qtd_estrelas=1)

# Configurações iniciais
run = True
screen_width = 720
screen_height = 480
clock = pg.time.Clock()
screen = pg.display.set_mode((screen_width, screen_height))
cenario = pg.image.load('src/assets/background.jpg')
test_surface = pg.Surface((160,30))
test_surface.fill('red')
test_rect = test_surface.get_rect(topleft = (200,280))

# Cria o grupo e adiciona o jogador
player = pg.sprite.GroupSingle()
player.add(Player(5))
enemy = pg.sprite.GroupSingle()
enemy.add(Foes(2))

# Loop principal do jogo
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.blit(cenario, (0, 0))
    enemy.draw(screen)
    dropped_item = enemy.sprite.update()
    if dropped_item:
        coletaveis.add(dropped_item)
    player.draw(screen)
    player.update()
    screen.blit(player.sprite.mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), (50, 50))

    coletados = pg.sprite.spritecollide(player.sprite, coletaveis, True, pg.sprite.collide_mask)
    for coletado in coletados:
        player.sprite.add_item(coletado)

    if player.sprite.attacking:
        if pg.sprite.spritecollide(player.sprite, enemy, False, pg.sprite.collide_mask) :    
            enemy.sprite.was_hit = True
            # ItemColetavel(enemy.sprite.drop, enemy.sprite.rect.x, (enemy.sprite.rect.y-30))

    coletaveis.draw(screen)
    screen.blit(test_surface, test_rect)

    clock.tick(60)
    pg.display.flip()
