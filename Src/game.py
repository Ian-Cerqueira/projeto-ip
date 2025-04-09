import pygame as pg
import sys
from classe_Button import Button
from classe_player import Player
from coletaveis_01 import ItemColetavel

# Configurações da tela e fonts
largura_tela = 1000
altura_tela = 720
tela = pg.display.set_mode((largura_tela, altura_tela))
pg.display.set_caption("ChronoCIn")
pixel_font = pg.font.Font("Src/Pixeltype.ttf", 40)
title_font = pg.font.Font("Src/Pixeltype.ttf", 100)

def primeira_fase():
    def criar_itens(qtd_moedas, qtd_chaves, qtd_estrelas):
        grupo = pg.sprite.Group()
        for _ in range(qtd_moedas): 
            grupo.add(ItemColetavel('moeda', 170, 350))
        for _ in range(qtd_chaves): 
            grupo.add(ItemColetavel('chave', 280, 350))
        for _ in range(qtd_estrelas): 
            grupo.add(ItemColetavel('estrela', 400, 250))
        return grupo

    coletaveis = criar_itens(qtd_moedas=1, qtd_chaves=1, qtd_estrelas=1)

    # Configurações iniciais da fase
    run = True
    clock = pg.time.Clock()
    # Cria uma nova superfície para a fase
    screen = pg.display.set_mode((largura_tela, altura_tela))
    cenario = pg.image.load('src/assets/background.jpg')
    cenario = pg.transform.scale(cenario, (largura_tela, altura_tela))

    # Cria o grupo e adiciona o jogador
    player = pg.sprite.GroupSingle()
    player.add(Player(5))

    fonte = pg.font.SysFont('Arial', 30)
    qtd_moedas = fonte.render(f"{player.sprite.inventario['moeda']}", True, (255, 255, 255))
    qtd_chave = fonte.render(f"{player.sprite.inventario['chave']}", True, (255, 255, 255))
    qtd_estrela = fonte.render(f"{player.sprite.inventario['estrela']}", True, (255, 255, 255))

    # Loop principal da fase
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Verifica se a tecla ESC foi pressionada para voltar ao menu
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

        screen.blit(cenario, (0, 0))
        screen.blit(qtd_moedas, (20, 60))
        screen.blit(qtd_chave, (20, 80))
        screen.blit(qtd_estrela, (20, 100))
        player.draw(screen)
        player.update()

        coletados = pg.sprite.spritecollide(player.sprite, coletaveis, True)
        for coletado in coletados:
            player.sprite.add_item(coletado)

        coletaveis.draw(screen)

        clock.tick(60)
        pg.display.flip()

    # Retorna ao menu quando sair da fase
    menu()

def menu():
    clock = pg.time.Clock()
    
    # Carrega o background de menu e ajusta a tela
    menu_background = pg.image.load("Src/assets/background_menu.jpg")
    menu_background = pg.transform.scale(menu_background, (largura_tela, altura_tela))
    
    # Renderiza o título do menu
    menu_text = title_font.render("ChronoCIn", True, "white")
    menu_text_rect = menu_text.get_rect(center=(500, 80))
    
    # Carrega a imagem do botão e redimensiona
    button_image = pg.image.load("Src/assets/Button.png")
    button_image = pg.transform.scale(button_image, (205, 84))
    
    # Cria os botões Play e Quit
    button_play = Button(button_image, 500, 300, "Play")
    button_quit = Button(button_image, 500, 500, "Quit")
    
    run = True
    while run:
        mouse_pos = pg.mouse.get_pos()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                # Se o mouse clicar sobre o botão Play, inicia a primeira fase
                if button_play.rect.collidepoint(mouse_pos):
                    primeira_fase()
                # Se o mouse clicar sobre o botão Quit, encerra o programa
                if button_quit.rect.collidepoint(mouse_pos):
                    run = False

        # Desenha o background e o título do menu
        tela.blit(menu_background, (0, 0))
        tela.blit(menu_text, menu_text_rect)
        
        # Atualiza a cor dos botões conforme a posição do mouse e os desenha
        for button in (button_play, button_quit):
            button.mudar_cor(mouse_pos)
            button.update(tela)
        
        pg.display.update()
        clock.tick(60)
    
    pg.quit()
    sys.exit()

menu()
