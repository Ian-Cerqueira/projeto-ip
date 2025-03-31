import pygame as pg

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, velocidade):
        super().__init__()

        # Carrega as sprite sheets
        self.sprite_sheet_run_right = pg.image.load("RunRight.png").convert_alpha()
        self.sprite_sheet_run_left = pg.transform.flip(self.sprite_sheet_run_right, True, False)
        self.sprite_sheet_idle_right = pg.image.load("IdleRight.png").convert_alpha()
        self.sprite_sheet_idle_left = pg.transform.flip(self.sprite_sheet_idle_right, True, False)
        self.sprite_sheet_idle_attack_right = pg.image.load("IdleAttack_Right.png").convert_alpha()
        self.sprite_sheet_idle_attack_left = pg.transform.flip(self.sprite_sheet_idle_attack_right, True, False)
        self.sprite_sheet_run_attack_right = pg.image.load("Run_attack.png").convert_alpha()
        self.sprite_sheet_run_attack_left = pg.transform.flip(self.sprite_sheet_run_attack_right, True, False)

        self.speed = velocidade
        self.frames = self.get_sprite_sheet(6, self.sprite_sheet_idle_right)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(100, 50))
        self.player_index = 0
        self.gravity = 0
        self.last_pos = 0  # Inicia com idle_right
        self.attacking = False

    def player_input(self):

        keys = pg.key.get_pressed()

        if any(keys) :
            if keys[pg.K_w]:
                self.player_jump()

            if keys[pg.K_SPACE]:
                if not self.attacking:
                    self.player_attack()
                    self.attacking = False

            if keys[pg.K_a]:
                self.rect.x -= self.speed
                self.last_pos = 2  # Movendo para a esquerda
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_left)

            if keys[pg.K_d]:
                self.rect.x += self.speed
                self.last_pos = 0  # Movendo para a direita
                self.frames = self.get_sprite_sheet(6, self.sprite_sheet_run_right)

        else:
            if self.last_pos == 2:
                self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_left)
            else:
                self.frames = self.get_sprite_sheet(4, self.sprite_sheet_idle_right)

    def definir_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400:
            self.rect.bottom = 400

    def player_jump(self):
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

# Configurações iniciais
run = True
clock = pg.time.Clock()
screen = pg.display.set_mode((720, 480))
cenario = pg.image.load('background.jpg')

# Cria o grupo e adiciona o jogador
player = pg.sprite.GroupSingle()
player.add(Player(5))

# Loop principal do jogo
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.blit(cenario, (0, 0))
    player.draw(screen)
    player.update()

    clock.tick(50)
    pg.display.flip()
