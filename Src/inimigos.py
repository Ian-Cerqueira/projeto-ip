import pygame as pg
from coletaveis import ItemColetavel
import random

pg.init()

inimigos = ('Punk', 'Biker')

class Foes(pg.sprite.Sprite):
    def __init__(self, velocidade, pos_x, pos_y, left_limit, right_limit, item_dropavel):
        super().__init__()
        escolha_inimigo = random.randint(0, 1)
        self.sprite_sheet_run_right = pg.image.load(f"assets/{inimigos[escolha_inimigo]}_run.png").convert_alpha()
        self.sprite_sheet_run_left = pg.transform.flip(self.sprite_sheet_run_right, True, False)
        self.sprite_sheet_idle_right = pg.image.load(f"assets/{inimigos[escolha_inimigo]}_idle.png").convert_alpha()
        self.sprite_sheet_idle_left = pg.transform.flip(self.sprite_sheet_idle_right, True, False)
        self.sprite_sheet_idle_attack_right = pg.image.load(f"assets/{inimigos[escolha_inimigo]}_punch.png").convert_alpha()
        self.sprite_sheet_idle_attack_left = pg.transform.flip(self.sprite_sheet_idle_attack_right, True, False)
        self.sprite_sheet_death = pg.image.load(f"assets/{inimigos[escolha_inimigo]}_death.png").convert_alpha()

        self.speed = velocidade
        # nao tem inventario
        self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_right)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))
        self.y_limit = pos_y
        self.x_limits = (left_limit, right_limit)
        self.mask = pg.mask.from_surface(self.image)
        self.player_index = 0
        self.gravity = 0
        self.last_pos = 0 # Inicia com idle_right
        self.attacking = False
        self.moving = False
        self.was_hit = False
        self.dead = False
        self.drop = item_dropavel
        self.item_was_drop = False

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
            if self.rect.x <= self.x_limits[0] or self.rect.x >= self.x_limits[1] :
                if self.rect.x >= self.x_limits[1]:
                    self.last_pos = 2
                else:
                    self.last_pos = 0

        if self.was_hit : # morreu
            self.frames = self.get_sprite_sheet(6, self.sprite_sheet_death)
            self.speed = 0
            # ItemColetavel(self.drop, self.rect.x, (self.rect.y-30))

    def definir_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.y_limit :
            self.rect.bottom = self.y_limit
    
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
        if self.was_hit == False :
            self.player_index += 0.2 # animação normal
        else:
            self.player_index += 0.15 # a animação da morte é um pouco mais lenta

        if self.player_index >= len(self.frames):
            self.player_index = 0
            if self.was_hit:
                self.dead = True  # Só marca como morto aqui

        if self.dead == False :
            self.image = self.frames[int(self.player_index)]
        else:
            self.image = self.frames[-1]


    def update(self):
        self.enemy_decision()
        self.animation_state()
        self.definir_gravity()
        if self.dead and not self.item_was_drop:
            self.item_was_drop = True
            item = ItemColetavel(self.drop, self.rect.centerx, self.rect.bottom - 50)
            return item