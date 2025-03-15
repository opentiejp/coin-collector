import pygame
import random

# 初期化
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Coin Collector Game")

# ステージ用
stage = 1

# 背景関連
bg_tile_image_files = ["Data/maptile_01.png", "Data/maptile_02.png", "Data/maptile_03.png", "Data/maptile_04.png"]
bg_tile_images = []
for bg_tile_image_file in bg_tile_image_files:
    bg_tile_image = pygame.image.load(bg_tile_image_file)
    bg_tile_image = pygame.transform.scale(bg_tile_image, [100, 100])
    bg_tile_images.append(bg_tile_image)

# プレイヤー関連
player_image = pygame.image.load("Data/player.png")  # 画像を読み込む
player_move_unit = 10  # プレイヤー移動時の単位距離
player_image_width = 100
player_image_height = round(player_image.get_height() / player_image.get_width() * player_image_width)
player_image = pygame.transform.scale(player_image, [player_image_width, player_image_height])  # 画像のサイズを指定する
player_rect = player_image.get_rect()  # Rect（四角）オブジェクトも生成しておく
player_rect.x = 50  # 初期位置
player_rect.y = 50  # 初期位置

# コイン関連
coins_number = 3  # コイン枚数の初期値
coin_image = pygame.image.load("Data/coin.png")  # 画像を読み込む
coin_image_width = round(player_image.get_width() / 1.6)
coin_image_height = round(coin_image.get_height() / coin_image.get_width() * coin_image_width)
coin_image = pygame.transform.scale(coin_image, [coin_image_width, coin_image_height])  # 画像のサイズを指定する
coins_rect = []  # Rect（四角）オブジェクトも生成しておく


def update_coins():
    for i in range(coins_number):
        x = random.randint(round(coin_image_width), round(screen_width - coin_image_width))
        y = random.randint(50, round(screen_height - coin_image_height))
        if i > 1:
            for j in range(i - 1):
                if (abs(coins_rect[j - 1][0] - x) < coin_image_width / 2) & (
                        abs(coins_rect[j - 1][1] - y) < coin_image_height / 3):  # 他のコインとほぼ重なっていたら別の位置にする
                    x = random.randint(round(coin_image_width), round(screen_width - coin_image_width))
                    y = random.randint(50, round(screen_height - coin_image_height))
        coins_rect.append(pygame.Rect(x, y, coin_image_width, coin_image_height))


update_coins()

# 宝石関連
gems_number = 0
gem_image = pygame.image.load("Data/gem.png")
gem_image_width = round(coin_image_width * 0.8)
gem_image_height = round(gem_image.get_height() / gem_image.get_width() * gem_image_width)
gem_image = pygame.transform.scale(gem_image, [gem_image_width, gem_image_height])
gems_rect = []


def update_gems():
    for i in range(round(gems_number)):
        x = random.randint(round(gem_image_width), round(screen_width - gem_image_width))
        y = random.randint(100, round(screen_height - gem_image_height))
        if i > 1:
            for j in range(i - 1):
                if (abs(gems_rect[j - 1][0] - x) < gem_image_width) & (
                        abs(gems_rect[j - 1][1] - y) < gem_image_height):  # 他の宝石とほぼ重なっていたら別の位置にする
                    x = random.randint(round(gem_image_width), round(screen_width - gem_image_width))
                    y = random.randint(100, round(screen_height - gem_image_height))
        gems_rect.append(pygame.Rect(x, y, gem_image_width, gem_image_height))


update_gems()

# スコア用
collected_coins = 0
collected_gems = 0
score = 0
font = pygame.font.Font(None, 36)
text = font.render(f"Score: {score}", True, (255, 255, 255))

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # キー操作を受け付けてプレイヤーを動かす
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_rect.x >= player_move_unit:
            player_rect.x -= player_move_unit
    if keys[pygame.K_RIGHT]:
        if (player_rect.x + player_image_width) <= screen_width - player_move_unit:
            player_rect.x += player_move_unit
    if keys[pygame.K_UP]:
        if player_rect.y >= 60:
            player_rect.y -= 10
    if keys[pygame.K_DOWN]:
        if (player_rect.y + player_image_height) <= screen_height - player_move_unit:
            player_rect.y += 10

    # プレイヤーがコインに触れた時の処理
    for coin_rect in coins_rect:
        if player_rect.colliderect(coin_rect):
            coins_rect.remove(coin_rect)
            collected_coins += 1
            score += 100

    # プレイヤーが宝石に触れた時の処理
    for gem_rect in gems_rect:
        if player_rect.colliderect(gem_rect):
            gems_rect.remove(gem_rect)
            collected_gems += 1
            score += 500

    # 背景色を塗りつぶす
    screen.fill("black")

    # 背景を描画  
    for x in range(round(screen_width / 100)):
        for y in range(round(screen_height / 100)):
            bg_tile = pygame.Rect(x * 100, y * 100, 100, 100)
            screen.blit(bg_tile_images[(stage - 1) % 4], bg_tile)  # 4ステージごとに背景画像をループ

    # スコアを表示    
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, [10, 10])

    # コイン・宝石とプレイヤーを描画
    for coin_rect in coins_rect:
        screen.blit(coin_image, coin_rect)
    for gem_rect in gems_rect:
        screen.blit(gem_image, gem_rect)
    screen.blit(player_image, player_rect)
    pygame.display.update()

    # ステージクリア時の処理
    if collected_coins == coins_number:
        stage += 1
        coins_number += 1
        collected_coins = 0
        update_coins()
        gems_rect = []  # 未取得の宝石は消えてしまう
        gems_number += 0.5  # 各ステージでの宝石数は徐々に増やす
        collected_gems = 0
        update_gems()
    if stage == 30:
        running = False

# ゲーム終了
pygame.quit()
