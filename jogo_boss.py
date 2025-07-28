import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_SPEED = 5
BOSS_SPEED = 2
PLATFORM_SPEED = 2
GRAVITY = 0.8
JUMP_STRENGTH = -16

background_img = pygame.image.load("assets/fundo_jogo.png").convert()
player_img_r = pygame.image.load("assets/viking-r.png").convert_alpha()
player_img_l = pygame.image.load("assets/viking-l.png").convert_alpha()
player_q1_r = pygame.image.load("assets/viking-r1-mc.png").convert_alpha()
player_q2_r = pygame.image.load("assets/viking-r2-mc.png").convert_alpha()
player_q1_l = pygame.image.load("assets/viking-l1-mc.png").convert_alpha()
player_q2_l = pygame.image.load("assets/viking-l2-mc.png").convert_alpha()
boss_img_r1 = pygame.image.load("assets/dragao-r1-mc.png").convert_alpha()
boss_img_l1 = pygame.image.load("assets/dragao-l1-mc.png").convert_alpha()
boss_img_r2 = pygame.image.load("assets/dragao-r2-mc.png").convert_alpha()
boss_img_l2 = pygame.image.load("assets/dragao-l2-mc.png").convert_alpha()
boss_fire_l = pygame.image.load("assets/dragao-fogo-l1-mc.png").convert_alpha()
power_img = pygame.image.load("assets/fogo3.png").convert_alpha()
platform_img = pygame.image.load("assets/plataforma2.png").convert_alpha()

font = pygame.font.SysFont(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img_r
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 140
        self.speed_y = 0
        self.facing_right = True
        self.on_ground = False
        self.lives = 5
        self.attacking = False
        self.attack_timer = 0
        self.attack_stage = 0
        self.has_hit_boss = False

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT]:
            dx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            dx = PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_UP] and self.on_ground:
            self.speed_y = JUMP_STRENGTH

        self.speed_y += GRAVITY
        self.rect.x += dx
        self.rect.y += self.speed_y

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        now = pygame.time.get_ticks()
        if self.attacking:
            if self.attack_stage == 0:
                self.image = player_q1_r if self.facing_right else player_q1_l
                self.attack_stage = 1
                self.attack_timer = now
            elif self.attack_stage == 1 and now - self.attack_timer > 150:
                self.image = player_q2_r if self.facing_right else player_q2_l
                self.attack_stage = 2
                self.attack_timer = now
            elif self.attack_stage == 2 and now - self.attack_timer > 150:
                self.image = player_img_r if self.facing_right else player_img_l
                self.attacking = False
                self.attack_stage = 0
                self.has_hit_boss = False  # libera novo hit
        else:
            self.image = player_img_r if self.facing_right else player_img_l

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_img_l1
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 150
        self.rect.y = HEIGHT - 90
        self.facing_right = False
        self.health = 10
        self.fire_timer = pygame.time.get_ticks()
        self.attack_timer = pygame.time.get_ticks()
        self.state = 0  # 0: idle, 1: attack, 2: fire

    def update(self):
        if self.facing_right:
            self.rect.x += BOSS_SPEED
            if self.rect.right >= WIDTH - 50:
                self.facing_right = False
        else:
            self.rect.x -= BOSS_SPEED
            if self.rect.left <= 400:
                self.facing_right = True

        now = pygame.time.get_ticks()
        distance = abs(player.rect.centerx - self.rect.centerx)

        if distance < 150:
            # alternar estados quando perto
            if now % 3000 < 1000:
                self.image = boss_img_r1 if self.facing_right else boss_img_l1
            elif now % 3000 < 2000:
                self.image = boss_img_r2 if self.facing_right else boss_img_l2
            else:
                self.image = boss_fire_l if not self.facing_right else boss_img_r2
        else:
            self.image = boss_img_r1 if self.facing_right else boss_img_l1

        if now - self.fire_timer >= 10000:
            fire = Power(self.rect.centerx, self.rect.centery, -6 if not self.facing_right else 6)
            boss_powers.add(fire)
            all_sprites.add(fire)
            self.fire_timer = now

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = PLATFORM_SPEED

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x):
        super().__init__()
        self.image = power_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
boss_powers = pygame.sprite.Group()

player = Player()
boss = Boss()
platform = Platform(WIDTH//2 - 100, HEIGHT//2 + 200)

all_sprites.add(player, boss, platform)
platforms.add(platform)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and not player.attacking:
                player.attacking = True

    all_sprites.update()

    if pygame.sprite.collide_rect(player, platform):
        if player.speed_y >= 0 and player.rect.bottom <= platform.rect.bottom:
            player.rect.bottom = platform.rect.top
            player.speed_y = 0
            player.on_ground = True
            player.rect.x += platform.speed_x

    if pygame.sprite.spritecollide(player, boss_powers, True):
        player.lives -= 1

    # hit control para somente 1 hit por ataque
    if player.attacking and not player.has_hit_boss:
        if abs(player.rect.centerx - boss.rect.centerx) < 100 and abs(player.rect.centery - boss.rect.centery) < 80:
            boss.health -= 1
            player.has_hit_boss = True

    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)

    lives_text = font.render(f"Lives: {player.lives}", True, BLACK)
    health_text = font.render(f"Boss HP: {boss.health}", True, BLACK)
    screen.blit(lives_text, (10, 10))
    screen.blit(health_text, (10, 40))

    pygame.display.flip()

    if player.lives <= 0 or boss.health <= 0:
        running = False

pygame.quit()
sys.exit()