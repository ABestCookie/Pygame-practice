
import pygame
import pygame.font
import pygame.mixer
import pygame.time
import pygame.display

import random
import os
import sys

def resource_path(relative_path):
    """支援 Nuitka / 開發環境載入資源"""
    try:
        base_path = sys._MEIPASS  # Nuitka/onefile 暫存資料夾
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()

# -- 基本參數 --
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

# -- 載入精靈圖 --
sheet = pygame.image.load(resource_path("assets/dino.png")).convert_alpha()

# 擷取 Dino 動畫
dino_run = [
    sheet.subsurface(pygame.Rect(936, 0, 44, 47)),
    sheet.subsurface(pygame.Rect(980, 0, 44, 47))
]
dino_dead = sheet.subsurface(pygame.Rect(1024, 0, 44, 47))
game_over_image = sheet.subsurface(pygame.Rect(655, 14, 190, 15))
cactus_image = sheet.subsurface(pygame.Rect(228, 2, 17, 35))

# -- 恐龍類別 --
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = dino_run
        self.dead_image = dino_dead
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - 90
        self.index = 0
        self.anim_timer = 0
        self.vel_y = 0
        self.gravity = 1.2
        self.is_jumping = False
        self.is_dead = False

    def update(self):
        if self.is_dead:
            self.image = self.dead_image
            return

        # 動畫跑步
        self.anim_timer += 1
        if not self.is_jumping and self.anim_timer >= 6:
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.anim_timer = 0

        # 跳躍
        if self.is_jumping:
            self.vel_y += self.gravity
            self.rect.y += self.vel_y
            if self.rect.y >= HEIGHT - 90:
                self.rect.y = HEIGHT - 90
                self.is_jumping = False
                self.vel_y = 0

    def jump(self):
        if not self.is_jumping and not self.is_dead:
            self.is_jumping = True
            self.vel_y = -15

# -- 障礙物類別 --
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cactus_image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(100, 300)
        self.rect.y = HEIGHT - 70
        self.speed = 6

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# -- 初始化物件 --
dino = Dino()
dino_group = pygame.sprite.GroupSingle(dino)
obstacle_group = pygame.sprite.Group()
spawn_timer = 0
game_over = False

# -- 主迴圈 --
running = True
while running:
    clock.tick(FPS)
    screen.fill((255, 255, 255))

    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over:
                    # 重啟遊戲
                    dino = Dino()
                    dino_group = pygame.sprite.GroupSingle(dino)
                    obstacle_group.empty()
                    game_over = False
                else:
                    dino.jump()

    # 更新邏輯
    if not game_over:
        dino_group.update()
        obstacle_group.update()

        # 生成障礙物
        spawn_timer += 1
        if spawn_timer >= 90:
            spawn_timer = 0
            obstacle_group.add(Cactus())

        # 碰撞檢測
        if pygame.sprite.spritecollide(dino, obstacle_group, False):
            dino.is_dead = True
            game_over = True

    # 畫圖
    dino_group.draw(screen)
    obstacle_group.draw(screen)

    if game_over:
        screen.blit(game_over_image, (WIDTH // 2 - 191 // 2, 50))

    pygame.display.flip()

pygame.quit()
