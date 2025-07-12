import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flona Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

ALTURA_SALTO = -14
TEMPO_ENVIO_PODER_MONSTRO = 200
DISTANCIA_PAREDES_MONSTRO = 10
VIDAS_MONSTRO = 3
VELOCIDADE_MONSTRO = 3
TEMPO_ENTRE_DIAMANTES = 4000
ALCANCE_PODER_PLAYER = 300
TEMPO_MONSTRO_EXPLODINDO = 500
VELOCIDADE_PLATAFORMA = 2  # diminuída para suavidade

background_img = pygame.image.load("assets/fundo_jogo.png").convert()
player_img_r = pygame.image.load("assets/viking-r.png").convert_alpha()
player_img_l = pygame.image.load("assets/viking-l.png").convert_alpha()
player_q1_r = pygame.image.load("assets/viking-q1-r.png").convert_alpha()
player_q2_r = pygame.image.load("assets/viking-q2-r.png").convert_alpha()
player_q1_l = pygame.image.load("assets/viking-q1-l.png").convert_alpha()
player_q2_l = pygame.image.load("assets/viking-q2-l.png").convert_alpha()
monster_img_r = pygame.image.load("assets/monstro-r.png").convert_alpha()
monster_img_l = pygame.image.load("assets/monstro-l.png").convert_alpha()
power_img = pygame.image.load("assets/fogo3.png").convert_alpha()
player_power_img = pygame.image.load("assets/poder-viking.png").convert_alpha()
explosion_img = pygame.image.load("assets/explosao.png").convert_alpha()
platform_img = pygame.image.load("assets/plataforma2.png").convert_alpha()
diamont_img = pygame.image.load("assets/diamante.png").convert_alpha()

font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

def draw_text(text, font, color, surface, x, y):
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    rect.center = (x, y)
    surface.blit(txt, rect)

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
        self.q_animating = False
        self.q_stage = 0
        self.q_timer = 0

    def update(self):
        self.speed_y += 0.8
        keys = pygame.key.get_pressed()
        self.speed_x = 0

        if keys[pygame.K_LEFT]:
            self.speed_x = -5
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
            self.facing_right = True
        if keys[pygame.K_UP] and self.on_ground:
            self.speed_y = ALTURA_SALTO
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
        self.speed_x = VELOCIDADE_MONSTRO
        self.health = VIDAS_MONSTRO
        self.shoot_timer = 0
        self.facing_right = False
        self.exploding = False
        self.explosion_start = 0

    def update(self):
        if self.exploding:
            if pygame.time.get_ticks() - self.explosion_start > TEMPO_MONSTRO_EXPLODINDO:
                self.exploding = False
            else:
                self.image = explosion_img
                return

        self.rect.x += self.speed_x
        if self.rect.right > WIDTH + DISTANCIA_PAREDES_MONSTRO:
            self.speed_x *= -1
            self.facing_right = False
        elif self.rect.left < DISTANCIA_PAREDES_MONSTRO:
            self.speed_x *= -1
            self.facing_right = True

        self.image = monster_img_r if self.facing_right else monster_img_l

        self.shoot_timer += 1
        if self.shoot_timer > TEMPO_ENVIO_PODER_MONSTRO:
            power = Power(self.rect.centerx, self.rect.centery, -5 if not self.facing_right else 5, power_img)
            monster_powers.add(power)
            all_sprites.add(power)
            self.shoot_timer = 0

        hits = pygame.sprite.spritecollide(self, balls, True)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = platform_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = VELOCIDADE_PLATAFORMA

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed_x *= -1

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
        self.distance_travelled = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.image == player_power_img:
            self.distance_travelled += abs(self.speed_x)
            if self.distance_travelled >= ALCANCE_PODER_PLAYER:
                self.kill()
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

def reset_game():
    global all_sprites, platforms, balls, monster_powers, player_powers, player, monster, platform, last_ball_spawn_time, game_over, win
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    monster_powers = pygame.sprite.Group()
    player_powers = pygame.sprite.Group()

    player = Player()
    monster = Monster()
    platform = Platform(WIDTH//2 - 150, HEIGHT//2 + 235)

    all_sprites.add(player, monster, platform)
    platforms.add(platform)

    last_ball_spawn_time = pygame.time.get_ticks()
    game_over = False
    win = False

reset_game()

running = True
while running:
    clock.tick(60)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if WIDTH//2 - 100 < mouse_x < WIDTH//2 + 100 and HEIGHT//2 + 50 < mouse_y < HEIGHT//2 + 100:
                    reset_game()
        else:
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

    if not game_over:
        if len(balls) == 0 and now - last_ball_spawn_time > TEMPO_ENTRE_DIAMANTES:
            ball = Ball(random.randint(0, WIDTH - 40), player.rect.y + random.randint(-50, 50))
            balls.add(ball)
            all_sprites.add(ball)
            last_ball_spawn_time = now

        all_sprites.update()

        # Mover player junto com a plataforma se em cima
        if pygame.sprite.collide_rect(player, platform):
            if player.speed_y >= 0 and player.rect.bottom <= platform.rect.bottom:
                player.rect.bottom = platform.rect.top
                player.speed_y = 0
                player.on_ground = True
                player.rect.x += platform.speed_x  # move junto com a plataforma

        hits = pygame.sprite.spritecollide(player, balls, True)
        for hit in hits:
            player.powers += 1

        hits = pygame.sprite.spritecollide(monster, player_powers, True)
        for hit in hits:
            monster.health -= 1
            monster.exploding = True
            monster.explosion_start = pygame.time.get_ticks()
            hit.kill()
            if monster.health <= 0:
                game_over = True
                win = True

        hits = pygame.sprite.spritecollide(player, monster_powers, True)
        if hits or pygame.sprite.collide_rect(player, monster):
            game_over = True
            win = False

        screen.blit(background_img, (0, 0))
        all_sprites.draw(screen)
        monster_text = font.render(f"Vida do monstro: {monster.health}", True, BLACK)
        player_text = font.render(f"Poderes jogador: {player.powers}", True, BLACK)
        screen.blit(monster_text, (10, 10))
        screen.blit(player_text, (10, 40))

    else:
        screen.blit(background_img, (0, 0))
        message = "Você Venceu!" if win else "Você Perdeu!"
        draw_text(message, large_font, RED, screen, WIDTH//2, HEIGHT//2 - 50)
        pygame.draw.rect(screen, GRAY, (WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50))
        draw_text("Reiniciar", font, BLACK, screen, WIDTH//2, HEIGHT//2 + 75)

    pygame.display.flip()

pygame.quit()
sys.exit()
