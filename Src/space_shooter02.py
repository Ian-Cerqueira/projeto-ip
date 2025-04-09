import pygame
import random
import sys

pygame.init()

largura_tela = 1200
altura_tela = 720
tela = pygame.display.set_mode((largura_tela, altura_tela))
cenario = pygame.image.load("background_space.png")
cenario = pygame.transform.scale(cenario, (largura_tela, altura_tela))
pygame.mixer.music.load('Generic Spaceshooter Project Original Soundtrack 3.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
pygame.display.set_caption("Invasores Espaciais")
relogio = pygame.time.Clock()

#cores (podemos transformar num dicionario depois, só pra ficar mais modular)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)
CIANO = (0, 255, 255)

#classe do Jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave_player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 10
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade = 8
        self.vidas = 99999
        self.delay_tiro = 250  #milissegundos
        self.ultimo_tiro = pygame.time.get_ticks()
        self.pontuacao = 100
        self.powerup_tiro_duplo = False
        self.powerup_tiro_triplo = False
        self.tempo_powerup = 0

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        
        self.rect.x = max(0, min(self.rect.x, largura_tela - self.rect.width))
        
        #atualiza tempo dos powerups
        if self.powerup_tiro_duplo or self.powerup_tiro_triplo:
            self.tempo_powerup += relogio.get_time()
            if self.tempo_powerup >= 10000:  # 10 segundos
                self.powerup_tiro_duplo = False
                self.powerup_tiro_triplo = False
                self.tempo_powerup = 0

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.delay_tiro:
            self.ultimo_tiro = agora
            

            if self.powerup_tiro_triplo:
                #tiro triplo em leque
                pygame.mixer.Sound('Bass Drum__005.ogg').play()
                for deslocamento in [-20, 0, 20]:
                    tiro = Tiro(self.rect.centerx + deslocamento, self.rect.top)
                    tiro.velocidade_x = deslocamento / 10  #desvio lateral com base no deslocamento

                    todos_sprites.add(tiro)
                    tiros.add(tiro)

            elif self.powerup_tiro_duplo:
                #tiro duplo
                pygame.mixer.Sound('Bass Drum__001.ogg').play()
                for deslocamento in [-15, 15]:
                    tiro = Tiro(self.rect.centerx + deslocamento, self.rect.top)
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
            else:
                #tiro normal
                pygame.mixer.Sound('Bass Drum__006.ogg').play()
                tiro = Tiro(self.rect.centerx, self.rect.top)
                todos_sprites.add(tiro)
                tiros.add(tiro)

#classe dos inimigos (cometas)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, tipo_cometa):
        super().__init__()
        dic = {'1': 'cometa_gray.png',
               '2': 'cometa_gray_2.png',
               '3': 'cometa_Brown.png'}
        self.image = pygame.image.load(dic[tipo_cometa])
        if tipo_cometa == '1' :    
            self.image = pygame.transform.scale_by(self.image, 0.13)
        elif tipo_cometa == '2' :
            self.image = pygame.transform.scale_by(self.image, 0.2)
        else:
            self.image = pygame.transform.scale_by(self.image, 0.4)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura_tela - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.velocidade_y = random.randrange(1, 5)
        self.velocidade_x = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x

        if self.rect.top > altura_tela + 10 or self.rect.left < -25 or self.rect.right > largura_tela + 25:
            self.kill()

#classe dos tiros
class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(VERDE)
        # self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidade_y = -10
        self.velocidade_x = 0

    def update(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x
        if self.rect.bottom < 0 or self.rect.top > altura_tela or self.rect.left < 0 or self.rect.right > largura_tela:
            self.kill()

#classe dos powerups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, tipo, x=None, y=None):
        super().__init__()
        self.tipo = tipo
        
        if self.tipo == 'vida':
            self.image = pygame.transform.scale2x(pygame.image.load('life_up_nave.png'))
        elif self.tipo == 'pontos':
            self.image = pygame.transform.scale2x(pygame.image.load('50_points.png'))
        elif self.tipo == 'tiro_duplo':
            self.image = pygame.transform.scale2x(pygame.image.load('tiro_duplo.png'))
        elif self.tipo == 'tiro_triplo':
            self.image = pygame.transform.scale2x(pygame.image.load('tiro_triplo.png'))
        
        self.rect = self.image.get_rect()
        if x and y:
            self.rect.centerx = x
            self.rect.centery = y
        else:
            self.rect.x = random.randrange(largura_tela - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
        self.velocidade_y = 2

    def update(self):
        self.rect.y += self.velocidade_y
        if self.rect.top > altura_tela:
            self.kill()

#classe do inimigo chefe
class InimigoChefe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprite_rayquaza.png')
        self.rect = self.image.get_rect()
        self.rect.y = 50
        self.velocidade_x = 3
        self.direcao = 1
        self.vida_maxima = 200
        self.vida_atual = self.vida_maxima
        self.delay_tiro = 1000
        self.ultimo_tiro = pygame.time.get_ticks()
        
    def update(self):
        self.rect.x += self.velocidade_x * self.direcao
        
        if self.rect.right > largura_tela or self.rect.left < 0:
            self.direcao *= -1
        
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.delay_tiro:
            self.ultimo_tiro = agora
            self.atirar()
    
    def atirar(self):
        for angulo in [-30, 0, 30]:
            cometa = CometaChefe(self.rect.centerx, self.rect.bottom)
            cometa.velocidade_y = 5
            cometa.velocidade_x = angulo / 10
            todos_sprites.add(cometa)
            cometas_chefe.add(cometa)
    
    def desenhar_barra_vida(self, superficie):
        largura_barra = 100
        altura_barra = 10
        vida_ratio = self.vida_atual / self.vida_maxima
        largura_atual = largura_barra * vida_ratio
        
        barra_rect = pygame.Rect(self.rect.x + 45, self.rect.y - 15, largura_atual, altura_barra)
        fundo_rect = pygame.Rect(self.rect.x + 45, self.rect.y - 15, largura_barra, altura_barra)
        
        pygame.draw.rect(superficie, VERMELHO, fundo_rect)
        pygame.draw.rect(superficie, VERDE, barra_rect)
        pygame.draw.rect(superficie, BRANCO, fundo_rect, 2)

tipos = ['1', '2', '3']
class CometaChefe(pygame.sprite.Sprite): 
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('sprite_tiro_boss.png')
        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.velocidade_y = 3
        self.velocidade_x = 0
        self.dano = 1

    def update(self):
        self.rect.y += self.velocidade_y
        self.rect.x += self.velocidade_x

        if self.rect.top > altura_tela + 10 or self.rect.left < -25 or self.rect.right > largura_tela + 25: # modularizar largura e altura da tela
            self.kill()

#grupos de sprites
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
powerups = pygame.sprite.Group()
cometas_chefe = pygame.sprite.Group()
chefes = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()

###
cometas_chefe.add(CometaChefe(100, 100))
# inimigos.add(Inimigo(random.choice(tipos)))
player.add(Jogador())

'''jogador = Jogador()
todos_sprites.add(jogador)'''

#cria inimigos iniciais
for i in range(8):
    inimigo = Inimigo(random.choice(tipos))
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

tempo_spawn = 0
tempo_powerup = 0
jogo_terminado = False
spawn_chefe = False
fase_atual = 1
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
                player.sprite.atirar()
            if evento.key == pygame.K_r and jogo_terminado:
                jogo_terminado = False
                player.sprite.vidas = 3
                player.sprite.pontuacao = 0
                spawn_chefe = False
                player.sprite.powerup_tiro_duplo = False
                player.sprite.powerup_tiro_triplo = False

                for sprite in todos_sprites:
                    sprite.kill()

                for i in range(8):
                    inimigo = Inimigo(random.choice(tipos))
                    todos_sprites.add(inimigo)
                    inimigos.add(inimigo)
    
    if not jogo_terminado:
        todos_sprites.update()
        player.sprite.update()

        #aparece o chefe quando o jogador alcança 100 pontos
        if player.sprite.pontuacao >= 100 and not spawn_chefe and len(chefes) == 0:
            chefe = InimigoChefe()
            todos_sprites.add(chefe)
            chefes.add(chefe)
            spawn_chefe = True
        
        #colisões entre tiros e inimigos normais
        # colisoes = pygame.sprite.spritecollide(tiros.sprite, inimigos, True, pygame.sprite.collide_mask)
        colisoes = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        for colisao in colisoes:
            #pygame.mixer.Sound('Explosion1__003.ogg').play()
            pygame.mixer.Sound('Footstep1__001.ogg').play()
            player.sprite.pontuacao += 10
            #chance de dropar um powerup (10%) melhor aumentar até
            if random.random() < 0.9:
                tipos_powerup = ['vida', 'pontos', 'tiro_duplo', 'tiro_triplo']
                powerup = PowerUp(random.choice(tipos_powerup))
                powerup.rect.centerx = colisao.rect.centerx
                powerup.rect.centery = colisao.rect.centery
                todos_sprites.add(powerup)
                powerups.add(powerup)
            inimigo = Inimigo(random.choice(tipos))
            todos_sprites.add(inimigo)
            inimigos.add(inimigo)
        
        #colisões entre tiros e chefes
        if spawn_chefe:
            for chefe in chefes:
                colisoes_chefe = pygame.sprite.spritecollide(chefe, tiros, True)
                for tiro in colisoes_chefe:
                    pygame.mixer.Sound('Explosion1__003.ogg').play()
                    chefe.vida_atual -= 10
                    if chefe.vida_atual <= 0:
                        chefe.kill()
                        player.sprite.pontuacao += 100
                        spawn_chefe = False
                
        #colisões entre jogador e inimigos normais
        #colisoes = pygame.sprite.spritecollide(player.sprite, inimigos, True, pygame.sprite.collide_mask)
        colisoes = pygame.sprite.spritecollide(player.sprite, inimigos, True)
        for colisao in colisoes:
            player.sprite.vidas -= 1
            inimigo = Inimigo(random.choice(tipos))
            todos_sprites.add(inimigo)
            inimigos.add(inimigo)
            if player.sprite.vidas <= 0:
                jogo_terminado = True
        
        #colisões entre jogador e cometas do chefe
        #colisoes_cometa = pygame.sprite.spritecollide(player.sprite, cometas_chefe, True, pygame.sprite.collide_circle_ratio(0.7))
        colisoes_cometa = pygame.sprite.spritecollide(player.sprite, cometas_chefe, True, pygame.sprite.collide_mask)
        for cometa in colisoes_cometa[:]:
            player.sprite.vidas -= cometa.dano
            if player.sprite.vidas <= 0:
                jogo_terminado = True
        
        #colisões entre jogador e powerups
        colisoes = pygame.sprite.spritecollide(player.sprite, powerups, True)
        for powerup in colisoes:
            if powerup.tipo == 'vida':
                pygame.mixer.Sound('Powerup__005.ogg').play()
                player.sprite.vidas += 1
            elif powerup.tipo == 'pontos':
                pygame.mixer.Sound('Jump__010.ogg').play()
                player.sprite.pontuacao += 50
            elif powerup.tipo == 'tiro_duplo':
                pygame.mixer.Sound('Jump__005.ogg').play()                
                player.sprite.powerup_tiro_duplo = True
                player.sprite.powerup_tiro_triplo = False
                player.sprite.tempo_powerup = 0
            elif powerup.tipo == 'tiro_triplo':
                pygame.mixer.Sound('Jump__003.ogg').play()
                player.sprite.powerup_tiro_triplo = True
                player.sprite.powerup_tiro_duplo = False
                player.sprite.tempo_powerup = 0
        
        #spawn de inimigos ao longo do tempo (só na fase 1)
        if fase_atual == 1:
            tempo_spawn += 1
            if tempo_spawn > 60 and len(inimigos) < 10:
                tempo_spawn = 0
                inimigo = Inimigo(random.choice(tipos))
                todos_sprites.add(inimigo)
                inimigos.add(inimigo)
        
        #spawn de powerups ao longo do tempo
        tempo_powerup += 1
        if tempo_powerup > 300:
            tempo_powerup = 0
            if random.random() < 0.3:  # 30% de chance
                tipos_powerup = ['vida', 'pontos', 'tiro_duplo', 'tiro_triplo']
                powerup = PowerUp(random.choice(tipos_powerup))
                todos_sprites.add(powerup)
                powerups.add(powerup)
    
    tela.blit(cenario, (0, 0))
    todos_sprites.draw(tela)
    player.draw(tela)

    #desenha a barra de vida do chefe se ele estiver vivo
    if spawn_chefe:
        for chefe in chefes:
            chefe.desenhar_barra_vida(tela)
    
    #mostra a pontuação e vidas
    texto_pontuacao = fonte.render(f"Pontuação: {player.sprite.pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (10, 10))
    
    texto_vidas = fonte.render(f"Vidas: {player.sprite.vidas}", True, BRANCO)
    tela.blit(texto_vidas, (10, 50))
    
    #mostra powerups ativos
    y_deslocamento = 90
    if player.sprite.powerup_tiro_duplo:
        tempo_restante = max(0, (10000 - player.sprite.tempo_powerup) // 1000)
        texto_powerup = fonte.render(f"Tiro Duplo: {tempo_restante}s", True, CIANO)
        tela.blit(texto_powerup, (10, y_deslocamento))
        y_deslocamento += 30
    
    if player.sprite.powerup_tiro_triplo:
        tempo_restante = max(0, (10000 - player.sprite.tempo_powerup) // 1000)
        texto_powerup = fonte.render(f"Tiro Triplo: {tempo_restante}s", True, LARANJA)
        tela.blit(texto_powerup, (10, y_deslocamento))
    
    if jogo_terminado:
        texto_game_over = fonte.render("FIM DE JOGO! Pressione R para reiniciar", True, VERMELHO)
        rect_game_over = texto_game_over.get_rect(center=(largura_tela//2, altura_tela//2))
        tela.blit(texto_game_over, rect_game_over)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
