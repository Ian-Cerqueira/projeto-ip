#parte inial do pygame
import pygame
from pygame.locals import *
pygame.init()
from plataforma import Plataforma
from player import Player
from inimigos import Foes
from coletaveis import ItemColetavel

#definir taxa de quadros
clock = pygame.time.Clock()
fps = 100
fonte = pygame.font.Font(None, 36)
instante_dano = 0
game_over = False
pygame.mixer.music.load('assets/fase_1_soundtrack.mp3')
pygame.mixer.music.set_volume(0.04)
pygame.mixer.music.play(-1)

#definição de tela:
screen_largura = 1000
screen_altura = 720
tela = pygame.display.set_mode((screen_largura,screen_altura))
#exbir nome do jogo
pygame.display.set_caption("ChronoCIN")

tamanho_bloco = 20

#carregar imagens:
mapa = pygame.image.load("assets/bg_ref.png")
#predios_detalhados = pygame.image.load("assets/prediosdeatalhados.png")

plataformas = pygame.sprite.Group()
#plataformas.add(Plataforma(200, 280, 160, 20)) # plataforma de teste
QUADRADO = 20
plataformas.add(Plataforma(QUADRADO*21, QUADRADO*9, QUADRADO*15, QUADRADO))
plataformas.add(Plataforma(QUADRADO*0, QUADRADO*4, QUADRADO*7, QUADRADO))
plataformas.add(Plataforma(QUADRADO*10, QUADRADO*5, QUADRADO*2, QUADRADO))
plataformas.add(Plataforma(QUADRADO*16, QUADRADO*4, QUADRADO*2, QUADRADO))
plataformas.add(Plataforma(QUADRADO*0, QUADRADO*13, QUADRADO*15, QUADRADO))
plataformas.add(Plataforma(QUADRADO*21, QUADRADO*19, QUADRADO*16, QUADRADO))
plataformas.add(Plataforma(QUADRADO*37, QUADRADO*11, QUADRADO*2, QUADRADO))
plataformas.add(Plataforma(QUADRADO*37, QUADRADO*22, QUADRADO*3, QUADRADO))
plataformas.add(Plataforma(QUADRADO*0, QUADRADO*22, QUADRADO*15, QUADRADO))
plataformas.add(Plataforma(QUADRADO*0, QUADRADO*35, QUADRADO*50, QUADRADO)) # chao
plataformas.add(Plataforma(QUADRADO*15, QUADRADO*25, QUADRADO*4, QUADRADO))
plataformas.add(Plataforma(QUADRADO*20, QUADRADO*28, QUADRADO*16, QUADRADO)) # essa
plataformas.add(Plataforma(QUADRADO*38, QUADRADO*32, QUADRADO*7, QUADRADO))
plataformas.add(Plataforma(QUADRADO*40, QUADRADO*24, QUADRADO*5, QUADRADO))
plataformas.add(Plataforma(QUADRADO*46, QUADRADO*28, QUADRADO*4, QUADRADO))
plataformas.add(Plataforma(QUADRADO*39, QUADRADO*15, QUADRADO*11, QUADRADO))
plataformas.add(Plataforma(QUADRADO*41, QUADRADO*7, QUADRADO*9, QUADRADO))
plataformas.add(Plataforma(QUADRADO*23, QUADRADO*3, QUADRADO*11, QUADRADO))
plataformas.add(Plataforma(QUADRADO*0, QUADRADO*29, QUADRADO*15, QUADRADO))

def grade_desesenho():
    for linha in range (0,54):
        pygame.draw.line(tela, (255,255,255), (0,linha * tamanho_bloco), (screen_largura, linha * tamanho_bloco))
        pygame.draw.line(tela, (255,255,255), (linha * tamanho_bloco, 0), (linha * tamanho_bloco, screen_altura))

player = pygame.sprite.GroupSingle()
player.add(Player(5))

def criar_inimigos():
    grupo = pygame.sprite.Group()
    grupo.add(Foes(3, QUADRADO*2, QUADRADO*4, 0, QUADRADO*4, 'chave')) # inimigo especial com a chave
    grupo.add(Foes(3, QUADRADO*5, QUADRADO*22, 0, QUADRADO*11, 'moeda')) # baixo esquerda
    grupo.add(Foes(3, QUADRADO*26, QUADRADO*28, QUADRADO*20, QUADRADO*33, 'moeda')) # baixo meio
    grupo.add(Foes(3, QUADRADO*41, QUADRADO*24, QUADRADO*38, QUADRADO*41, 'moeda')) # plataforma curta
    grupo.add(Foes(3, QUADRADO*28, QUADRADO*19, QUADRADO*20, QUADRADO*33, 'moeda')) # alto meio
    grupo.add(Foes(3, QUADRADO*40, QUADRADO*15, QUADRADO*38, QUADRADO*47, 'moeda')) # alto direita
    grupo.add(Foes(3, QUADRADO*47, QUADRADO*7, QUADRADO*40, QUADRADO*47, 'moeda')) # altissimo direita
    return grupo
enemy = criar_inimigos()

def criar_itens(qtd_moedas, qtd_nave, qtd_vidas):
    grupo = pygame.sprite.Group()
    for _ in range(qtd_moedas): 
        if _ == 0 :    
            grupo.add(ItemColetavel('moeda', QUADRADO*10, QUADRADO*19))
        elif _ == 1 : 
            grupo.add(ItemColetavel('moeda', QUADRADO*10, QUADRADO*10))
        elif _ == 2 :
            grupo.add(ItemColetavel('moeda', QUADRADO*30, QUADRADO*16))
        elif _ == 3 :
            grupo.add(ItemColetavel('moeda', QUADRADO*26, QUADRADO*1))
        else:
            grupo.add(ItemColetavel('moeda', QUADRADO*10, QUADRADO*3))
    for _ in range(qtd_nave): 
        grupo.add(ItemColetavel('nave', QUADRADO*1, QUADRADO*21.5))
    for _ in range(qtd_vidas): 
        if _ == 0 :    
            grupo.add(ItemColetavel('vida', QUADRADO*28, QUADRADO*7))
        else:
            grupo.add(ItemColetavel('vida', QUADRADO*37.5, QUADRADO*20))
    return grupo

coletaveis = criar_itens(qtd_moedas=5, qtd_nave=1, qtd_vidas=2)

#classe que armazena e constroi o mapa atraves dos blocos
class World():
    
    def __init__(self, data):
        self.lista_bloco = []
        #carregar imagem
        varandinha = pygame.image.load("assets/bloco.png")
        linha_count = 0
        for linha in data:
            col_count = 0
            for bloco in linha:
                if bloco == 1:
                    img = pygame.transform.scale(varandinha, (tamanho_bloco, tamanho_bloco))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tamanho_bloco
                    img_rect.y = linha_count * tamanho_bloco
                    bloco = (img, img_rect)
                    self.lista_bloco.append(bloco)
                col_count += 1
            linha_count += 1

    def draw(self):
        for bloco in self.lista_bloco:
            tela.blit(bloco[0],bloco[1])
            pygame.draw.rect(tela,(255,255,255), bloco[1], 1)
#testeeeeeeeeeeeeee

#matriz do mapa
matriz_malha = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

mundo = World(matriz_malha)
#rodagem da tela/jogo
jogo_rodando = True

while jogo_rodando:
    
    #limita a taxa de fps
    clock.tick(fps)

    #exibir mapa de fundo
    tela.blit(mapa, (0,0))

    #desenha o mundo a partir da grade
    mundo.draw()

    #insere e atualiza o sprite do player
    
    if not game_over:
        player.sprite.update(plataformas)
        for i in range (len(enemy)) :
            dropped_item = enemy.sprites()[i].update()
            if dropped_item != None:
                break
        plataformas.draw(tela)
        pygame.draw.rect(tela, (255, 0, 0), player.sprite.rect_pes, 2)
        player.draw(tela)
        enemy.draw(tela)
        if dropped_item:
            coletaveis.add(dropped_item)
        coletaveis.draw(tela)

        #mantem a malha d edesenho
        #grade_desesenho()

        texto_moedas = fonte.render(f"Moedas: {player.sprite.inventario['moeda']}", True, (255, 0, 255))
        texto_chave = fonte.render(f"Chave: {player.sprite.inventario['chave']}", True, (255, 255, 0))
        texto_vida = fonte.render(f"Vidas: {player.sprite.health}", True, (255, 0, 0))
        tela.blit(texto_moedas, (20, 20))
        tela.blit(texto_chave, (20, 50))
        tela.blit(texto_vida, (20, 80))
    
        coletados = pygame.sprite.spritecollide(player.sprite, coletaveis, False, pygame.sprite.collide_mask)
        for coletado in coletados:
            if coletado.tipo == 'vida':
                if player.sprite.health < 3 :
                    
                    player.sprite.get_health()
                    coletaveis.remove(coletado)  # remove manualmente
            elif coletado.tipo == 'nave' :
                if player.sprite.inventario['chave'] == 1 :
                    texto_nave = fonte.render("Passou!", True, (0, 255, 0))
                    tela.blit(texto_nave, (screen_largura // 2, screen_altura // 2))
                # NÃO remove a nave aqui
            else:
                pygame.mixer.Sound('assets/Powerup__005.ogg').play()
                player.sprite.add_item(coletado)
                coletaveis.remove(coletado)  # remove manualmente


        for inimigo in enemy: 
            if pygame.sprite.collide_mask(player.sprite, inimigo):
                if player.sprite.attacking:    
                    inimigo.was_hit = True
                elif not inimigo.was_hit:
                    tempo_atual = pygame.time.get_ticks() # dá um tempo de 3 segundos de invencibilidade para o player apos tomar um hit
                    if tempo_atual - instante_dano > 3000 : # 3 segundos    
                        player.sprite.take_damage()
                        instante_dano = pygame.time.get_ticks()

        if player.sprite.dead :
            game_over = True

    #conicao para fechar o jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and game_over:
                game_over = False
                for coletavel in coletaveis :
                    coletavel.kill()
                coletaveis = criar_itens(qtd_moedas=5, qtd_nave=1, qtd_vidas=2)
                for en in enemy :
                    en.kill()
                enemy = criar_inimigos()
                player.sprite.kill()
                player.add(Player(5))

    if game_over :
        tela.fill('black')
        texto_game_over = fonte.render("FIM DE JOGO! Pressione R para reiniciar", True, (255, 0, 0))
        rect_game_over = texto_game_over.get_rect(center=(500, 350))
        tela.blit(texto_game_over, rect_game_over)

    pygame.display.update()

pygame.quit()