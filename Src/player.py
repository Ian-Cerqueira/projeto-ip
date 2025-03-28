import pygame as pg

pg.init()

# sprite class
class Player(pg.sprite.Sprite) :

    def __init__ (self, velocidade): # atributos que serão ligados ao personagem principal
        super().__init__() 
        self.Health_Points = 3
        # ideia futura
        # sprite_1 = pg.image.load...
        # sprite_2 = pg.image.load...
        # sprite_3 = pg.image.load...
        # self.player_run = [sprite_1, sprite_2, sprite_3]
        # self.player_index = 0
        # self.player_jump = pg.image.load...
        # self.image = self.player_run[self.player_index]
        #
        # isso irá permitir animar os sprites
        self.speed = velocidade
        self.image = pg.image.load("c:/users/ianda/downloads/image-removebg-preview.png")
        self.rect = self.image.get_rect(midbottom = (100,200))
        self.inventario = {'chave': 0, 'estrela': 0, 'moedas': 0}
        self.gravity = 0

    def player_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] :
            # pulo
            if # player pisando em um superficie :
                self.gravity = -20
        if keys[pg.K_a] :
            self.rect.x -= self.speed
        if keys[pg.K_d] :
            self.rect.x += self.speed
        if keys[pg.K_SPACE] :
            # ataque
        if keys[pg.K_l] :
            # arma especial

    def set_moedas(self) : # pegou moeda
        self.inventario['moedas'] += 1

    def set_chave(self) : # pegou A chave
        self.inventario['chave'] = 1

    def definir_gravity(self) :
        self.gravity += 1
        self.rect.y = self.gravity
        if self.rect.bottom # precisa estar em cima de uma superficie
            self.rect.bottom # nao pode cair da superficie atual
            self.gravity = 0 # zera a gravidade quando acima de uma superficie

    def update(self) :
        self.player_input()
        self.definir_gravity()
        self.animation_state()

    def animation_state(self) :
        if self.rect.bottom # quando estiver pulando
            self.image = self.player_jump
        else:
            self.player_index += 0.2 # transição gradual para novo sprite
            if self.player_index >= len(self.player_run) :
                self.player_index = 0 # completa o ciclo da animação
            self.image = self.player_run[int(self.player_index)]



x = Player(12)

print(x.__dict__)

# Player.draw(screen)
# Player.update()
