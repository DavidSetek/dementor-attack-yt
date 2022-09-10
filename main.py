import pygame
import random

# Inicializace hry
pygame.init()

# Obrazovka
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Utok mozkomora")

# Nastavení hry
fps = 60
clock = pygame.time.Clock()

# Hodnoty hry
player_start_lives = 5
mozkomor_start_speed = 2
mozkomor_speed_acceleration = 0.5
score = 0

player_lives = player_start_lives
mozkomor_speed = mozkomor_start_speed

mozkomor_x = random.choice([-1, 1])
mozkomor_y = random.choice([-1, 1])

# Obrázky
background_image = pygame.image.load("img/hogwarts-castle.jpg")
background_image_rect = background_image.get_rect()
background_image_rect.topleft = (0, 0)

mozkomor_image = pygame.image.load("img/mozkomor.png")
mozkomor_image_rect = mozkomor_image.get_rect()
mozkomor_image_rect.center = (width//2, height//2)

# Barvy
dark_yellow = pygame.Color("#938f0c")


# Fonty
potter_font_big = pygame.font.Font("fonts/Harry.ttf", 50)
potter_font_middle = pygame.font.Font("fonts/Harry.ttf", 30)

# Texty
score_text = potter_font_middle.render(f"Skore: {score}", True, dark_yellow)
score_text_rect = score_text.get_rect()
score_text_rect.topright = (width - 30, 10)

lives_text = potter_font_middle.render(f"Zivoty: {player_lives}", True, dark_yellow)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (width - 30, 50)

game_over_text = potter_font_big.render("Hra skoncila", True, dark_yellow)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (width//2, height//2)

continue_text = potter_font_middle.render("Klikni kamkoli pro pokracovani", True, dark_yellow)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (width//2, height//2 + 50)

# Zvuky
success_click = pygame.mixer.Sound("media/success_click.wav")
miss_click = pygame.mixer.Sound("media/miss_click.wav")
pygame.mixer.music.load("media/bg-music-hp.wav")
pygame.mixer.music.set_volume(0.1)
success_click.set_volume(0.05)
miss_click.set_volume(0.05)

# Hlavní cyklus
lets_continue = True
pygame.mixer.music.play(-1, 0.0)
while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x = event.pos[0]
            click_y = event.pos[1]

            # Bylo kliknuto na mozkomora
            if mozkomor_image_rect.collidepoint(click_x, click_y):
                success_click.play()
                score += 1
                mozkomor_speed += mozkomor_speed_acceleration

                # mozkomor_x = random.choice([-1, 1])
                # mozkomor_y = random.choice([-1, 1])

                previous_x = mozkomor_x
                previous_y = mozkomor_y

                while previous_x == mozkomor_x and previous_y == mozkomor_y:
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])
            else:
                miss_click.play()
                player_lives -= 1

    # Pohybujeme mozkomorem
    mozkomor_image_rect.x += mozkomor_x * mozkomor_speed
    mozkomor_image_rect.y += mozkomor_y * mozkomor_speed

    # Odraz mozkomora
    if mozkomor_image_rect.left < 0 or mozkomor_image_rect.right >= width:
        mozkomor_x = -1 * mozkomor_x
    elif mozkomor_image_rect.top < 0 or mozkomor_image_rect.bottom >= height:
        mozkomor_y = -1 * mozkomor_y

    # Updatujeme text skóre a životy
    score_text = potter_font_middle.render(f"Skore: {score}", True, dark_yellow)
    lives_text = potter_font_middle.render(f"Zivoty: {player_lives}", True, dark_yellow)

    # Obrázky
    screen.blit(background_image, background_image_rect)
    screen.blit(mozkomor_image, mozkomor_image_rect)

    # Texty
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)

    # Update obrazovky
    pygame.display.update()

    # Zpomalení cyklu (tikání hodin)
    clock.tick(fps)

    # Kontrola konce hry
    if player_lives == 0:
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()

        # Pozastavit hru do dalšího kliknutí
        pygame.mixer.music.stop()
        paused = True
        while paused:
            # chce hrát znovu?
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = player_start_lives
                    mozkomor_speed = mozkomor_start_speed
                    mozkomor_image_rect.center = (width//2, height//2)
                    mozkomor_x = random.choice([-1, 1])
                    mozkomor_y = random.choice([-1, 1])
                    pygame.mixer.music.play(-1, 0.0)
                    paused = False
                elif event.type == pygame.QUIT:
                    paused = False
                    lets_continue = False

# Ukončení hry
pygame.quit()


