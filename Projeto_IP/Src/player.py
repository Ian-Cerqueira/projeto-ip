import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, velocidade):
        super().__init__()

        # Carrega as sprite sheets
        self.sprite_sheet_run_right = pygame.image.load("assets/RunRight.png").convert_alpha()
        self.sprite_sheet_run_left = pygame.transform.flip(self.sprite_sheet_run_right, True, False)
        self.sprite_sheet_idle_right = pygame.image.load("assets/IdleRight.png").convert_alpha()
        self.sprite_sheet_idle_left = pygame.transform.flip(self.sprite_sheet_idle_right, True, False)
        self.sprite_sheet_idle_attack_right = pygame.image.load("assets/Idle_Attack.png").convert_alpha()
        self.sprite_sheet_idle_attack_left = pygame.transform.flip(self.sprite_sheet_idle_attack_right, True, False)
        self.sprite_sheet_run_attack_right = pygame.image.load("assets/Run_attack.png").convert_alpha()
        self.sprite_sheet_run_attack_left = pygame.transform.flip(self.sprite_sheet_run_attack_right, True, False)
        self.sprite_sheet_idle_jump_right = pygame.image.load("assets/Cyborg_jump.png").convert_alpha()
        self.sprite_sheet_idle_jump_left = pygame.transform.flip(self.sprite_sheet_idle_jump_right, True, False)

        self.speed = velocidade
        self.inventario = {'moeda': 0, 'chave': 0, 'estrela': 0}
        self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_right)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(100, 700))
        self.mask = pygame.mask.from_surface(self.image)
        self.player_index = 0
        self.gravity = 0
        self.last_pos = 0  # Inicia com idle_right
        self.jumping = False
        self.attacking = False
        self.moving = False
        self.health = 3
        self.dead = False
        self.step_sound = [pygame.mixer.Sound('assets/Footstep1__009.ogg'), pygame.mixer.Sound('assets/Footstep1__007.ogg')]
        self.step_idx = 0
        self.step_channel = pygame.mixer.Channel(1)
        self.old_rect = self.rect.copy()
        self.rect_pes = pygame.Rect(0, 0, 14 * 2, 2 * 2)  # Dobrando o tamanho como os sprites

    def atualizar_rect_pes(self):
        self.rect_pes.width = self.rect.width // 2
        self.rect_pes.height = 5
        if self.last_pos == 0 :    
            self.rect_pes.midtop = (self.rect.centerx, self.rect.bottom)
        else:
            self.rect_pes.midtop = (self.rect.centerx+32, self.rect.bottom - 2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        self.moving = False

        self.rect.x = max(-40, min(self.rect.x, 1000 - self.rect.width))

        if keys[pygame.K_w]:
            self.player_jump()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.moving = True
            self.last_pos = 2  # Esquerda
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.moving = True
            self.last_pos = 0  # Direita

        # Verifica se o jogador está atacando
        if keys[pygame.K_SPACE]:
            self.attacking = True
            self.atualizar_rect_pes()

            if self.moving:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_left)
                else:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_right)

                self.play_step_sound()

            else:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_left)
                else:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_right)
        else:
            self.attacking = False
            self.atualizar_rect_pes()
            
            if self.moving:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_left)
                else:
                    self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_right)
            
                self.play_step_sound()
            
            else:
                if self.last_pos == 2:
                    self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_left)
                    if self.jumping :
                        self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_jump_left)

                elif self.last_pos == 0:
                    self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_right)
                    if self.jumping :
                        self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_jump_right)

    def definir_gravity(self, plataformas):
        self.old_rect = self.rect.copy()
        self.gravity += 1
        self.rect.y += self.gravity
        self.atualizar_rect_pes()
        if self.rect.bottom >= 720:
            self.jumping = False

        for plataforma in plataformas:
            if self.rect_pes.colliderect(plataforma.rect) and self.gravity >= 0:
                if self.rect.bottom <= plataforma.rect.top or self.old_rect.bottom <= plataforma.rect.top :
                    self.rect.bottom = plataforma.rect.top
                    self.gravity = 0
                    self.jumping = False

    def player_jump(self):
        self.old_rect = self.rect.copy()
        if not self.jumping :
            self.jumping = True
            self.gravity = -17
            jump_sound = pygame.mixer.Sound('assets/Jump__005.ogg')
            jump_sound.set_volume(0.3)
            jump_sound.play()

    def player_attack(self):
        self.attacking = True

        self.atualizar_rect_pes()
        if self.last_pos == 2:
            if pygame.key.get_pressed()[pygame.K_a]:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_left)
            else:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_left)
        else:
            if pygame.key.get_pressed()[pygame.K_d]:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_attack_right)
            else:
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_attack_right)

    def take_damage(self):
        if self.health > 1 :
            pygame.mixer.Sound('assets/Snare__001.ogg').play()
            self.health -= 1 # tomou dano
        else:
            pygame.mixer.Sound('assets/Snare__010.ogg').play()
            self.health = 0
            self.dead = True

    def play_step_sound(self):
        if not self.jumping:
            if not self.step_channel.get_busy():
                self.step_channel.play(self.step_sound[self.step_idx])
                self.step_channel.set_volume(0.2)
                self.step_idx = (self.step_idx + 1) % len(self.step_sound)

    def get_health(self):
        if self.health < 3 :
            pygame.mixer.Sound('assets/heal_sound.mp3').play()
            self.health += 1 # pegou um coração e recuperou vida

    def display_hearts(self):
        pass

    def add_item(self, item):
        if item.tipo in self.inventario:
            self.inventario[item.tipo] += 1
            print(f'Coletou {item.tipo}. Inventário: {self.inventario}')
            
    def get_sprite_sheet(self, num_frames, sheet):
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height

        for idx in range(num_frames):
            # Extrai o frame original (48x48)
            frame = sheet.subsurface(pygame.Rect(idx * frame_width, 0, frame_width, frame_height)).copy()
            # Redimensiona o frame para o dobro do tamanho: 96x96
            scaled_frame = pygame.transform.scale(frame, (frame_width * 2, frame_height * 2))
            frames.append(scaled_frame)
        return frames

    def animation_state(self):
        # Atualiza o índice da animação de forma gradual
        self.player_index += 0.2
        if self.player_index >= len(self.frames):
            self.player_index = 0
            if self.attacking :
                pygame.mixer.Sound('assets/punch_in_air.mp3').play()

        # Atualiza a imagem para o frame atual
        self.image = self.frames[int(self.player_index)]

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, plataformas):
        self.player_input()
        self.definir_gravity(plataformas)
        self.animation_state()
        self.display_hearts()
        self.atualizar_rect_pes()