import pygame
import random
import sys

pygame.init()

#configurações da tela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Invasores Espaciais")
relogio = pygame.time.Clock()

#cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)

#classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 10
        self.velocidade = 8
        self.vidas = 3
        self.delay_tiro = 250  #milissegundos
        self.ultimo_tiro = pygame.time.get_ticks()
        self.pontuacao = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        
        #mantém o jogador na tela
        self.rect.x = max(0, min(self.rect.x, largura_tela - self.rect.width))

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.delay_tiro:
            self.ultimo_tiro = agora
            tiro = Tiro(self.rect.centerx, self.rect.top)
            todos_sprites.add(tiro)
            tiros.add(tiro)

#classe dos Inimigos (cometas)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura_tela - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidade_y = random.randrange(1, 5)
        self.velocidade_x = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x

        #morre se sair da tela
        if self.rect.top > altura_tela + 10 or self.rect.left < -25 or self.rect.right > largura_tela + 25:
            self.kill()

#classe dos Tiros
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidade_y = -10

    def update(self):
        self.rect.y += self.velocidade_y
        #remove se sair da tela
        if self.rect.bottom < 0:
            self.kill()

#classe dos itens coletáveis
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tipo = random.choice(['vida', 'pontos', 'velocidade'])
        
        if self.tipo == 'vida':
            self.image = pygame.Surface((25, 25))
            self.image.fill(ROXO)
        elif self.tipo == 'pontos':
            self.image = pygame.Surface((25, 25))
            self.image.fill(AMARELO)
        else:  # velocidade
            self.image = pygame.Surface((25, 25))
            self.image.fill(BRANCO)
            
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura_tela - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidade_y = random.randrange(1, 3)

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.top > altura_tela:
            self.kill()

#classe do inimigo Chefe
class InimigoChefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 60))
        self.image.fill(ROXO)
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.y = 50
        self.velocidade_x = 3
        self.direcao = 1  #1 para direita e -1 para esquerda
        self.vida_maxima = 200
        self.vida_atual = self.vida_maxima
        self.delay_tiro = 1000
        self.ultimo_tiro = pygame.time.get_ticks()
        
    def update(self):
        #move pra direita se o direçao for 1 e pra esquerda quando for -1
        self.rect.x += self.velocidade_x * self.direcao
        
        #inverte a direção quando bater na borda do mapa
        if self.rect.right > largura_tela or self.rect.left < 0:
            self.direcao *= -1
        
        #logica do tiro, o tempo depois do tiro for maior que o delay ele pode atirar de novo
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.delay_tiro:
            self.ultimo_tiro = agora
            self.atirar()
    
    def atirar(self):
        #cria 3 balas em diferentes direções
        for angulo in [-30, 0, 30]:
            cometa = CometaChefe(self.rect.centerx, self.rect.bottom)
            cometa.velocidade_y = 5
            cometa.velocidade_x = angulo / 10
            todos_sprites.add(cometa)
            cometas_chefe.add(cometa)
    
    def desenhar_barra_vida(self, superficie):

        #calcula o tamanho da barra
        largura_barra = 100
        altura_barra = 10
        vida_ratio = self.vida_atual / self.vida_maxima
        largura_atual = largura_barra * vida_ratio
        
        #coloquei a barra acima do boss
        barra_rect = pygame.Rect(self.rect.x, self.rect.y - 15, largura_atual, altura_barra)
        fundo_rect = pygame.Rect(self.rect.x, self.rect.y - 15, largura_barra, altura_barra)
        
        #desenha a barra
        pygame.draw.rect(superficie, VERMELHO, fundo_rect)
        pygame.draw.rect(superficie, VERDE, barra_rect)
        pygame.draw.rect(superficie, BRANCO, fundo_rect, 2)

class CometaChefe(Inimigo):
    def __init__(self, x, y):
        super().__init__()
        self.rect.centerx = x
        self.rect.centery = y
        self.image.fill(AMARELO)
        self.velocidade_y = 5
        self.velocidade_x = 0
        self.dano = 2

#grupos de sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
powerups = pygame.sprite.Group()
cometas_chefe = pygame.sprite.Group()
chefes = pygame.sprite.Group()

jogador = Jogador()
todos_sprites.add(jogador)

# Cria inimigos iniciais
for i in range(8):
    inimigo = Inimigo()
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

tempo_spawn = 0
tempo_powerup = 0
jogo_terminado = False
spawn_chefe = False
fonte = pygame.font.SysFont('Arial', 30)

#loop principal
rodando = True
while rodando:
    relogio.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                jogador.atirar()
            if evento.key == pygame.K_r and jogo_terminado:
                jogo_terminado = False
                jogador.vidas = 3
                jogador.pontuacao = 0
                spawn_chefe = False

                for sprite in todos_sprites:
                    sprite.kill()

                jogador = Jogador()
                todos_sprites.add(jogador)

                for i in range(8):
                    inimigo = Inimigo()
                    todos_sprites.add(inimigo)
                    inimigos.add(inimigo)
    
    if not jogo_terminado:
        todos_sprites.update()
        
        #aparece o chefe quando o jogador alcança 100 pontos
        if jogador.pontuacao >= 100 and not spawn_chefe and len(chefes) == 0:
            chefe = InimigoChefe()
            todos_sprites.add(chefe)
            chefes.add(chefe)
            spawn_chefe = True
        
        #colisões entre tiros e inimigos normais
        colisoes = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        for colisao in colisoes:
            jogador.pontuacao += 10
            #cChance de dropar um powerup
            if random.random() > 0.9:  # 10% de chance
                powerup = PowerUp()
                todos_sprites.add(powerup)
                powerups.add(powerup)
            inimigo = Inimigo()
            todos_sprites.add(inimigo)
            inimigos.add(inimigo)
        
        #colisões entre tiros e chefes
        if spawn_chefe:
            for chefe in chefes:
                colisoes_chefe = pygame.sprite.spritecollide(chefe, tiros, True)
                for tiro in colisoes_chefe:
                    chefe.vida_atual -= 10
                    if chefe.vida_atual <= 0:
                        chefe.kill()
                        jogador.pontuacao += 100
                        spawn_chefe = False
        
        #colisões entre jogador e inimigos normais
        colisoes = pygame.sprite.spritecollide(jogador, inimigos, True)
        for colisao in colisoes:
            jogador.vidas -= 1
            inimigo = Inimigo()
            todos_sprites.add(inimigo)
            inimigos.add(inimigo)
            if jogador.vidas <= 0:
                jogo_terminado = True
        
        #colisões entre jogador e cometas do chefe
        colisoes_cometa = pygame.sprite.spritecollide(jogador, cometas_chefe, True)
        for cometa in colisoes_cometa:
            jogador.vidas -= cometa.dano
            if jogador.vidas <= 0:
                jogo_terminado = True
        
        #colisões entre jogador e powerups
        colisoes = pygame.sprite.spritecollide(jogador, powerups, True)
        for colisao in colisoes:
            if colisao.tipo == 'vida':
                jogador.vidas += 1
            elif colisao.tipo == 'pontos':
                jogador.pontuacao += 50
            else:  #velocidade
                jogador.velocidade += 1
        
        #spawn de inimigos ao longo do tempo
        tempo_spawn += 1
        if tempo_spawn > 60:
            tempo_spawn = 0
            inimigo = Inimigo()
            todos_sprites.add(inimigo)
            inimigos.add(inimigo)
        
        #spawn de powerups ao longo do tempo
        tempo_powerup += 1
        if tempo_powerup > 300:
            tempo_powerup = 0
            if random.random() > 0.7:  # 30% de chance
                powerup = PowerUp()
                todos_sprites.add(powerup)
                powerups.add(powerup)
    
    tela.fill(PRETO)
    todos_sprites.draw(tela)
    
    #desenha a barra de vida do chefe se ele existir
    if spawn_chefe:
        for chefe in chefes:
            chefe.desenhar_barra_vida(tela)
    
    #mostra a pontuação e vidas
    texto_pontuacao = fonte.render(f"Pontuação: {jogador.pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (10, 10))
    
    texto_vidas = fonte.render(f"Vidas: {jogador.vidas}", True, BRANCO)
    tela.blit(texto_vidas, (10, 50))
    
    if jogo_terminado:
        texto_game_over = fonte.render("FIM DE JOGO! Pressione R para reiniciar", True, VERMELHO)
        tela.blit(texto_game_over, (largura_tela//2 - 180, altura_tela//2))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
