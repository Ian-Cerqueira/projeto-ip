import pygame as pg

pg.init()

class Foes(pg.sprite.Sprite):
    def __init__(self, velocidade):
        super().__init__()
        self.sprite_sheet_run_right = pg.image.load("Src/assets/Punk_run.png").convert_alpha()
        self.sprite_sheet_run_left = pg.transform.flip(self.sprite_sheet_run_right, True, False)
        self.sprite_sheet_idle_right = pg.image.load("Src/assets/Punk_idle.png").convert_alpha()
        self.sprite_sheet_idle_left = pg.transform.flip(self.sprite_sheet_idle_right, True, False)
        self.sprite_sheet_idle_attack_right = pg.image.load("Src/assets/Punk_punch.png").convert_alpha()
        self.sprite_sheet_idle_attack_left = pg.transform.flip(self.sprite_sheet_idle_attack_right, True, False)
        self.sprite_sheet_death = pg.image.load("Src/assets/Punk_death.png").convert_alpha()

        self.speed = velocidade
        # nao tem inventario
        self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_right)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(600, 50))
        self.mask = pg.mask.from_surface(self.image)
        self.player_index = 0
        self.gravity = 0
        self.last_pos = 0 # Inicia com idle_right
        self.attacking = False
        self.moving = False
        self.was_hit = False
        self.dead = False
        self.drop = 'chave'

    ########################################################
    def enemy_decision(self):
        self.moving = True
        if self.moving:
            if self.last_pos == 2:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_left)
                self.rect.x -= self.speed
                self.last_pos = 2  # Esquerda
            else:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_right)
                self.rect.x += self.speed
                self.last_pos = 0  # Direita
            if self.rect.x <= 0 or self.rect.x >= 720 :
                if self.rect.x >= 720:
                    self.last_pos = 2
                else:
                    self.last_pos = 0

        if self.was_hit : # morreu
            self.frames = self.get_sprite_sheet(6, self.sprite_sheet_death)
            self.speed = 0
            self.drop

    def definir_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400   
    
    def enemy_attack(self):
        self.attacking = True

        if self.last_pos == 2:
            self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_left)
        else:
            self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_right)

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
        if self.was_hit == False :    
            self.player_index += 0.2 # animação normal
        else:
            self.player_index += 0.15 # a animação da morte é um pouco mais lenta
        if self.player_index >= len(self.frames):
            self.player_index = 0
            if self.was_hit == True :
                self.dead = True

        # Atualiza a imagem para o frame atual
        if self.dead == False : 
            self.image = self.frames[int(self.player_index)]
        else:
            self.image = self.frames[-1]

    def update(self):
        self.enemy_decision()
        self.animation_state()
        self.definir_gravity()