import pygame as pg
import sys
from parallax import ParallaxVertical
from typing_text import TypingText
from primeira_fase import jogo_1

def scene_lore():
    pg.init()
    
    LORE = '''Em um futuro próximo, um jovem estudante do CIN, obcecado por inovação, se depara com um problema aparentemente insolúvel. Durante suas pesquisas, ele descobre que precisa de um item essencial para concluir seu projeto, algo tão avançado que ainda não existe em sua época. Frustrado, ele recorre a uma IA altamente desenvolvida, que analisa uma vasta quantidade de dados históricos e aponta uma única solução: o item que ele busca será criado em uma época diferente da sua. Ajude-o na sua aventura!'''

    WIDTH = 1000
    HEIGHT = 720
    FPS = 60 

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    title = pg.display.set_caption("ChronoCIN")
    clock = pg.time.Clock()
    bg_image = pg.image.load("assets/space.png")
    stars_image = pg.image.load("assets/stars.png")                                                   
    running = 1

    space = ParallaxVertical(bg_image, 1, WIDTH, HEIGHT)
    stars = ParallaxVertical(stars_image, 2, WIDTH, HEIGHT)

    lore_text = TypingText(LORE, "courier", 30, 80, WIDTH)

    while running:
        clock.tick(FPS)
        
        for event in pg.event.get():
            if(event.type == pg.QUIT):
                pg.quit()
            if(event.type == pg.KEYDOWN) and lore_text.isFinished():
                return True
        
        space.update(screen)
        stars.update(screen)
        lore_text.draw(screen, (20, 170))
        lore_text.update()
            
        pg.display.flip()
        

    sys.exit()
    