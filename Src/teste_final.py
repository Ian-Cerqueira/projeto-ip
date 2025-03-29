import pygame as pg

pg.init()

class Player(pg.sprite.Sprite) :

    def __init__ (self, velocidade): # atributos que serão ligados ao personagem principal
        super().__init__() 
        self.Health_Points = 3
        run_right = pg.transform.scale2x((pg.image.load('sprite_sheets/RunRight.png'))).convert_alpha()
        run_left = pg.transform.scale2x((pg.image.load('sprite_sheets/RunLeft.png'))).convert_alpha()
        idle_right = pg.transform.scale2x((pg.image.load('sprite_sheets/IdleRight.png'))).convert_alpha()
        idle_left = pg.transform.scale2x((pg.image.load('sprite_sheets/IdleLeft.png'))).convert_alpha()
        # (x_sprite * 48, 0, 48, 48)
        self.player_run = [idle_right, run_right, idle_left, run_left]
        self.player_index = 0
        self.speed = velocidade
        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,50))
        self.inventario = {'chave': 0, 'estrela': 0, 'moedas': 0}
        self.gravity = 0
        self.last_pos = 0 # inicia o player na sprite idle_right

    
    def player_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a] :
            self.rect.x -= self.speed
            self.image = self.player_run[3]
            self.last_pos = 2
            self.player_jump()
        
        elif keys[pg.K_d] :
            self.rect.x += self.speed
            self.image = self.player_run[1]
            self.last_pos = 0
            self.player_jump()

        elif keys[pg.K_w] :
            self.player_jump()

        else:
            if self.last_pos == 2 :
                self.image = self.player_run[2]
            else:
                self.image = self.player_run[0]
    
    def definir_gravity(self) :
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400 :
            self.rect.bottom = 400

    def player_jump (self) :
        keys = pg.key.get_pressed()
        if keys[pg.K_w] :
            if self.rect.bottom >= 400 :
                self.gravity = -20

    def update(self) :
        self.player_input()
        self.definir_gravity()

    #def animation_state(self) :
    #    self.player_index += 0.2 # transição gradual para novo sprite
    #    if self.player_index >= len(self.player_run) :
    #        self.player_index = 0 # completa o ciclo da animação
    #    self.image = self.player_run[int(self.player_index)]


run = True
clock = pg.time.Clock()

screen = pg.display.set_mode((720,480))

cenario = pg.image.load('sprite_sheets/background.jpg')

# group
player = pg.sprite.GroupSingle()
player.add(Player(5))

while run:
    for event in pg.event.get() :
        if event.type == pg.QUIT :
            run = False

       
    

    screen.blit(cenario, (0,0))
    player.draw(screen)
    player.update()


    clock.tick(50)
    pg.display.flip() 