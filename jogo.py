import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load images
background_img = pygame.image.load("assets/fundo_jogo.png").convert()
# background_img = pygame.image.load("assets/palmares2.png").convert()

# Player images
player_img_r = pygame.image.load("assets/viking-r.png").convert_alpha()
player_img_l = pygame.image.load("assets/viking-l.png").convert_alpha()
player_q1_r = pygame.image.load("assets/viking-q1-r.png").convert_alpha()
player_q2_r = pygame.image.load("assets/viking-q2-r.png").convert_alpha()
player_q1_l = pygame.image.load("assets/viking-q1-l.png").convert_alpha()
player_q2_l = pygame.image.load("assets/viking-q2-l.png").convert_alpha()

# Monster images
monster_img_r = pygame.image.load("assets/monstro-r.png").convert_alpha()
monster_img_l = pygame.image.load("assets/monstro-l.png").convert_alpha()

# Power images
power_img = pygame.image.load("assets/fogo3.png").convert_alpha()
player_power_img = pygame.image.load("assets/poder-viking.png").convert_alpha()

platform_img = pygame.image.load("assets/plataforma2.png").convert_alpha()
diamont_img = pygame.image.load("assets/diamante.png").convert_alpha()

font = pygame.font.SysFont(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img_r
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 50
        self.speed_x = 0
        self.speed_y = 0
        self.on_ground = False
        self.powers = 0
        self.facing_right = True

        # Q animation control
        self.q_animating = False
        self.q_stage = 0
        self.q_timer = 0

    def update(self):
        self.speed_y += 0.8  # gravity
        keys = pygame.key.get_pressed()
        self.speed_x = 0

        if keys[pygame.K_LEFT]:
            self.speed_x = -5
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
            self.facing_right = True
        if keys[pygame.K_UP] and self.on_ground:
            self.speed_y = -12
        if keys[pygame.K_DOWN]:
            self.speed_y += 0.5

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # Handle Q animation: change once per stage, then return to normal
        if self.q_animating:
            now = pygame.time.get_ticks()
            if self.q_stage == 0:
                self.image = player_q1_r if self.facing_right else player_q1_l
                self.q_stage = 1
                self.q_timer = now
            elif self.q_stage == 1 and now - self.q_timer > 150:
                self.image = player_q2_r if self.facing_right else player_q2_l
                self.q_stage = 2
                self.q_timer = now
            elif self.q_stage == 2 and now - self.q_timer > 150:
                self.image = player_img_r if self.facing_right else player_img_l
                self.q_animating = False
                self.q_stage = 0
        else:
            self.image = player_img_r if self.facing_right else player_img_l

class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = monster_img_l
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = HEIGHT - 73
        self.speed_x = 2
        self.health = 10
        self.shoot_timer = 0
        self.facing_right = False

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.speed_x *= -1
            self.facing_right = False
        elif self.rect.left < WIDTH // 2:
            self.speed_x *= -1
            self.facing_right = True

        self.image = monster_img_r if self.facing_right else monster_img_l

        self.shoot_timer += 1
        if self.shoot_timer > 130:
            power = Power(self.rect.centerx, self.rect.centery, -5 if not self.facing_right else 5, power_img)
            monster_powers.add(power)
            all_sprites.add(power)
            self.shoot_timer = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = diamont_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Power(pygame.sprite.Sprite):
    def __init__(self, x, y, speed_x, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = speed_x

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
balls = pygame.sprite.Group()
monster_powers = pygame.sprite.Group()
player_powers = pygame.sprite.Group()

player = Player()
monster = Monster()
platform = Platform(WIDTH//2 - 150, HEIGHT//2 + 225)

all_sprites.add(player, monster, platform)
platforms.add(platform)

last_ball_spawn_time = pygame.time.get_ticks()

running = True
while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and player.powers > 0:
                power = Power(player.rect.centerx, player.rect.centery, 7 if player.facing_right else -7, player_power_img)
                player_powers.add(power)
                all_sprites.add(power)
                player.powers -= 1
            if event.key == pygame.K_q:
                if not player.q_animating:
                    player.q_animating = True
                    player.q_stage = 0

    # Spawn diamante a cada 10s se não houver nenhum em cena
    if len(balls) == 0 and now - last_ball_spawn_time > 10000:
        ball = Ball(random.randint(0, WIDTH - 40), player.rect.y + random.randint(-50, 50))
        balls.add(ball)
        all_sprites.add(ball)
        last_ball_spawn_time = now

    all_sprites.update()

    if pygame.sprite.spritecollide(player, platforms, False):
        if player.speed_y > 0:
            player.rect.bottom = platform.rect.top
            player.speed_y = 0
            player.on_ground = True

    hits = pygame.sprite.spritecollide(player, balls, True)
    for hit in hits:
        player.powers += 1

    hits = pygame.sprite.spritecollide(monster, player_powers, True)
    for hit in hits:
        monster.health -= 1
        hit.kill()
        if monster.health <= 0:
            print("You Win!")
            running = False

    hits = pygame.sprite.spritecollide(player, monster_powers, True)
    if hits:
        print("You Lose!")
        running = False

    if pygame.sprite.collide_rect(player, monster):
        print("You Lose!")
        running = False

    screen.blit(background_img, (0, 0)) 
    all_sprites.draw(screen)

    # Mostrar HUD
    monster_text = font.render(f"Monstro Vida: {monster.health}", True, BLACK)
    player_text = font.render(f"Player Poder: {player.powers}", True, BLACK)
    screen.blit(monster_text, (10, 10))
    screen.blit(player_text, (10, 40))

    pygame.display.flip()

pygame.quit()
sys.exit()
