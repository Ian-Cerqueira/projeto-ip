import pygame as pg

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, velocidade):
        super().__init__()

        # Carrega as sprite sheets
        self.sprite_sheet_run_right = pg.image.load("src/assets/RunRight.png").convert_alpha()
        self.sprite_sheet_run_left = pg.transform.flip(self.sprite_sheet_run_right, True, False)
        self.sprite_sheet_idle_right = pg.image.load("src/assets/IdleRight.png").convert_alpha()
        self.sprite_sheet_idle_left = pg.transform.flip(self.sprite_sheet_idle_right, True, False)
        self.sprite_sheet_idle_attack_right = pg.image.load("src/assets/Idle_Attack.png").convert_alpha()
        self.sprite_sheet_idle_attack_left = pg.transform.flip(self.sprite_sheet_idle_attack_right, True, False)
        self.sprite_sheet_run_attack_right = pg.image.load("src/assets/Run_attack.png").convert_alpha()
        self.sprite_sheet_run_attack_left = pg.transform.flip(self.sprite_sheet_run_attack_right, True, False)
        self.sprite_sheet_idle_jump_right = pg.image.load("src/assets/Cyborg_jump.png").convert_alpha()
        self.sprite_sheet_idle_jump_left = pg.transform.flip(self.sprite_sheet_idle_jump_right, True, False)
        self.sprite_sheet_heart = pg.image.load("Src/assets/life_heart.jpeg").convert_alpha()

        self.speed = velocidade
        self.inventario = {'moeda': 0, 'chave': 0, 'estrela': 0}
        self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_right)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(100, 50))
        self.mask = pg.mask.from_surface(self.image)
        self.player_index = 0
        self.gravity = 0
        self.last_pos = 0  # Inicia com idle_right
        self.jumping = False
        self.attacking = False
        self.moving = False
        self.health = 3


    def player_input(self):

        keys = pg.key.get_pressed()
        self.moving = False

        if keys[pg.K_w]:
            self.player_jump()

        if keys[pg.K_a]:
            self.rect.x -= self.speed
            self.moving = True
            self.last_pos = 2  # Esquerda
        elif keys[pg.K_d]:
            self.rect.x += self.speed
            self.moving = True
            self.last_pos = 0  # Direita

        # Verifica se o jogador está atacando
        if keys[pg.K_SPACE]:
            self.attacking = True

            if self.moving:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_left)
                else:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_right)

            else:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_left)
                else:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_right)
        else:
            self.attacking = False
            
            if self.moving:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_left)
                else:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_right)
            else:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_left)
                    if self.jumping :
                        self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_jump_left)

                elif self.last_pos == 0:
                    self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_right)
                    if self.jumping :
                        self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_jump_right)

    def definir_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.jumping = False
            self.rect.bottom = 400

    def player_jump(self):
        self.jumping = True
        if self.rect.bottom >= 400:
            self.gravity = -20

    def player_attack(self):
        self.attacking = True

        if self.last_pos == 2:
            if pg.key.get_pressed()[pg.K_a]:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_left)
            else:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_left)
        else:
            if pg.key.get_pressed()[pg.K_d]:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_right)
            else:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_right)

    def get_damage(self):
        if self.health > 0 :
            self.health -= 1 # tomou dano
        
    def get_health(self):
        if self.health < 3 :
            self.health += 1 # pegou um coração e recuperou vida

    def display_hearts(self):
        pass

    def add_item(self, item):
        if item.tipo in self.inventario:
            self.inventario[item.tipo] += 1
            print(f'Coletou {item.tipo}. Inventário: {self.inventario}')

    '''def checkcollisions_x (self):
        if self.moving :
            if pg.Rect.colliderect(self.rect, test_rect):
                self.rect.x = 200'''
            
    def get_sprite_sheet(self, num_frames, sheet):
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height

        for idx in range(num_frames):
            # Extrai o frame original (48x48)
            frame = sheet.subsurface(pg.Rect(idx * frame_width, 0, frame_width, frame_height)).copy()
            # Redimensiona o frame para o dobro do tamanho: 96x96
            scaled_frame = pg.transform.scale(frame, (frame_width * 2, frame_height * 2))
            frames.append(scaled_frame)
        return frames

    def animation_state(self):
        # Atualiza o índice da animação de forma gradual
        self.player_index += 0.2
        if self.player_index >= len(self.frames):
            self.player_index = 0

        # Atualiza a imagem para o frame atual
        self.image = self.frames[int(self.player_index)]

    def update(self):
        self.player_input()
        self.definir_gravity()
        self.animation_state()
        self.display_hearts()
        '''self.checkcollisions_x()'''
        '''self.checkcollisions_y()'''