import pygame
import sys
import random
from tkinter import Tk, messagebox

# Inițializare Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Dimensiunea ferestrei
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mage Power")

# Culori și fonturi
background_color = (30, 30, 30)
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)
highlight_color = (0, 200, 200)
text_color = (255, 255, 255)

# Resurse audio
collision_sound = pygame.mixer.Sound("assets/Music/collision.wav")
powerup_sound = pygame.mixer.Sound("assets/Music/powerup.wav")
game_over_sound = pygame.mixer.Sound("assets/Music/gameover.wav")
destroy_powerup_sound = pygame.mixer.Sound("assets/Music/destroy.wav")

pygame.mixer.music.set_volume(0.5)
collision_sound.set_volume(0.5)
powerup_sound.set_volume(0.5)
game_over_sound.set_volume(0.5)

# Resurse imagini
player_image = pygame.image.load("assets/Characters/character.png")
player_image = pygame.transform.scale(player_image, (75, 75))

enemy_image = pygame.image.load("assets/Characters/enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (75, 75))

enemy_runner_image = pygame.image.load("assets/Characters/enemy_runner.png")
enemy_runner_image = pygame.transform.scale(enemy_runner_image, (75, 75))

enemy_zigzag_image = pygame.image.load("assets/Characters/enemy_zigzag.png")
enemy_zigzag_image = pygame.transform.scale(enemy_zigzag_image, (75, 75))

powerup_image = pygame.image.load("assets/Characters/power_up.png")
powerup_image = pygame.transform.scale(powerup_image, (75, 75))

destroy_all_powerup_image = pygame.image.load("assets/Characters/destroy_all.jpg")
destroy_all_powerup_image = pygame.transform.scale(destroy_all_powerup_image, (75, 75))

heart_image = pygame.image.load("assets/Characters/heart.webp")
heart_image = pygame.transform.scale(heart_image, (30, 30))

game_background_image=pygame.image.load("assets/Characters/game_background_image.png")
game_background_image=pygame.transform.scale(game_background_image,(SCREEN_WIDTH,SCREEN_HEIGHT))

# Background image
main_menu_background = pygame.image.load("assets/Characters/main_menu.png")
main_menu_background = pygame.transform.scale(main_menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Game menu image
game_menu_background=pygame.image.load("assets/Characters/game_menu.jpeg")
game_menu_background=pygame.transform.scale(game_menu_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Buttons images
start_button=pygame.image.load("assets/Characters/start_button.png")
start_button=pygame.transform.scale(start_button, (300,150))

leaderboard_button=pygame.image.load("assets/Characters/leaderboard_button.png")
leaderboard_button=pygame.transform.scale(leaderboard_button, (300,150))

settings_button=pygame.image.load("assets/Characters/settings_button.png")
settings_button=pygame.transform.scale(settings_button, (300,150))

exit_button=pygame.image.load("assets/Characters/exit_button.png")
exit_button=pygame.transform.scale(exit_button, (300,150))

BUTTON_WIDTH,BUTTON_HEIGHT=start_button.get_width(),start_button.get_height()
BUTTON_SPACING=5

start_x=(SCREEN_WIDTH-BUTTON_WIDTH)//5
start_y = SCREEN_HEIGHT//5

# Enemy types
enemy_types = [
    {"name": "basic", "speed": 1, "image": enemy_image},
    {"name": "runner", "speed": 2, "image": enemy_runner_image},
    {"name": "zigzag", "speed": 1, "image": enemy_zigzag_image}
]

# Leaderboard
leaderboard_file = "leaderboard.txt"
def load_leaderboard():
    try:
        with open(leaderboard_file, "r") as file:
            return [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        return []

def save_to_leaderboard(score):
    scores = load_leaderboard()
    scores.append(score)
    scores = sorted(scores, reverse=True)[:5]
    with open(leaderboard_file, "w") as file:
        for s in scores:
            file.write(f"{s}\n")

def show_game_over_message():
    pygame.mixer.Sound.play(game_over_sound)
    root = Tk()
    root.withdraw()
    messagebox.showinfo("Game Over", "Game Over! Apasă OK pentru a reveni la meniul principal.")
    root.destroy()

# Setări globale
volume = 0.5
difficulty = "Medium"

def settings_menu():
    global volume, difficulty

    options = ["Volume", "Difficulty", "Back"]
    selected_option = 0
    difficulty_levels = ["Easy", "Medium", "Hard"]
    current_difficulty_index = difficulty_levels.index(difficulty)

    while True:
        screen.fill(background_color)

        # Titlul meniului de setări
        title_text = font.render("Settings", True, text_color)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        for i, option in enumerate(options):
            color = highlight_color if i == selected_option else text_color
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 100))
            screen.blit(text, text_rect)

        # Afișare valoare pentru opțiuni
        if selected_option == 0:  # Volume
            volume_text = small_font.render(f"Volume: {int(volume * 100)}%", True, text_color)
            screen.blit(volume_text, (SCREEN_WIDTH // 3 - 300, SCREEN_HEIGHT // 3))
        elif selected_option == 1:  # Difficulty
            difficulty_text = small_font.render(f"Difficulty: {difficulty}", True, text_color)
            screen.blit(difficulty_text, (SCREEN_WIDTH // 5 - 300, SCREEN_HEIGHT // 5 + 200))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 2:  # Back
                        return
                elif event.key == pygame.K_LEFT:
                    if selected_option == 0:  # Adjust volume
                        volume = max(0.0, volume - 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif selected_option == 1:  # Adjust difficulty
                        current_difficulty_index = (current_difficulty_index - 1) % len(difficulty_levels)
                        difficulty = difficulty_levels[current_difficulty_index]
                elif event.key == pygame.K_RIGHT:
                    if selected_option == 0:  # Adjust volume
                        volume = min(1.0, volume + 0.1)
                        pygame.mixer.music.set_volume(volume)
                    elif event.key == 1:  # Adjust difficulty
                        current_difficulty_index = (current_difficulty_index + 1) % len(difficulty_levels)
                        difficulty = difficulty_levels[current_difficulty_index]

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Meniu principal
def main_menu():
    pygame.mixer.music.load("assets/Music/main_menu.mp3")
    pygame.mixer.music.play(-1)

    selected_option = 0
    options = ["Start a New Game", "Leaderboard", "Settings", "Exit"]

    buttons = [
    {"image": start_button, "rect": pygame.Rect(start_x, start_y, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"image": leaderboard_button, "rect": pygame.Rect(start_x, start_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)},
    {"image": exit_button, "rect": pygame.Rect(start_x, start_y + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)},
]

    # Calculăm înălțimea totală a butoanelor și spațiilor dintre ele
    total_height = (len(options) * BUTTON_HEIGHT + (len(options) - 1) * BUTTON_SPACING)//4
    top_margin = (SCREEN_HEIGHT - total_height) // 2  # Poziționăm butoanele pe verticală în mijloc

    # Calculăm pozițiile butoanelor pe axa X și Y
    button_rects = [
        pygame.Rect(SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, top_margin + (BUTTON_HEIGHT +BUTTON_SPACING) * i, BUTTON_WIDTH, BUTTON_HEIGHT)
        for i in range(len(options))
    ]

    while True:
        # Afișează imaginea de fundal
        screen.blit(main_menu_background, (0, 0))

        # Desenează butoanele
        for i, rect in enumerate(button_rects):
            # Folosim imagini pentru butoane, fiecare corespunzând opțiunii
            button_image = start_button if i == 0 else leaderboard_button if i == 1 else settings_button if i == 2 else exit_button
            screen.blit(button_image, rect.topleft)

            # Evidențierea butonului selectat
            if i == selected_option:
                # Adăugăm o bordură groasă și culoare de evidențiere
                pygame.draw.rect(screen, highlight_color, rect.inflate(10, 10), 5)  # Creștem dimensiunea rect-ului pentru a face evidențierea mai vizibilă
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        game_loop()
                    elif selected_option == 1:
                        show_leaderboard()
                    elif selected_option == 2:
                        settings_menu()
                    elif selected_option == 3:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Leaderboard
def show_leaderboard():
    scores = load_leaderboard()
    back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 150, 200, 50)

    while True:
        screen.fill(background_color)
        title = font.render("Leaderboard", True, text_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        for i, score in enumerate(scores):
            score_text = small_font.render(f"{i + 1}. {score}", True, text_color)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, 200 + i * 50))

        pygame.draw.rect(screen, (50, 50, 50), back_button_rect)
        pygame.draw.rect(screen, text_color, back_button_rect, 2)
        back_text = small_font.render("Back", True, text_color)
        back_text_rect = back_text.get_rect(center=back_button_rect.center)
        screen.blit(back_text, back_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return

        pygame.display.flip()
        pygame.time.Clock().tick(60)

# Meniu de pauză
def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    paused = False
                elif event.key == pygame.K_m:
                    main_menu()
                    return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        pause_text = font.render("Paused", True, text_color)
        resume_text = small_font.render("Press TAB to Resume", True, text_color)
        menu_text = small_font.render("Press M for Main Menu", True, text_color)

        screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(resume_text, (SCREEN_WIDTH // 2 - resume_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Joc propriu-zis
def game_loop():
    pygame.mixer.music.load("assets/Music/gameplay.mp3")
    pygame.mixer.music.play(-1)


    square_x, square_y = 100, 200
    square_speed = 3

    enemy_size = 35
    enemy_speed = 1
    spawn_rate = 50
    powerup_spawn_chance = 1500
    shield, lives = 100, 3  # Vieți inițiale setate la 3
    life_powerups = []
    destroy_all_powerups = []
    enemies = []

    score = 0
    last_score_update = pygame.time.get_ticks()
    difficulty_timer = pygame.time.get_ticks()
    spawn_timer = 0
    screen.blit(game_menu_background, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and square_x > 0:
            square_x -= square_speed
        if keys[pygame.K_d] and square_x + 75 < SCREEN_WIDTH:
            square_x += square_speed
        if keys[pygame.K_w] and square_y > 0:
            square_y -= square_speed
        if keys[pygame.K_s] and square_y + 75 < SCREEN_HEIGHT:
            square_y += square_speed
        if keys[pygame.K_ESCAPE]:
            pause_menu()

        player_rect = pygame.Rect(square_x, square_y, 75, 75)

        screen.blit(game_background_image, (0, 0))

        spawn_timer += 1
        if spawn_timer > spawn_rate:
            for _ in range(min(4, 1 + score // 20)):
                side = random.choice(["top", "bottom", "left", "right"])
                enemy_type = random.choice(enemy_types)
                speed = enemy_type["speed"]
                image = enemy_type["image"]
                enemy_data = {
                    "type": enemy_type["name"],
                    "x": 0, "y": 0, "dx": 0, "dy": 0,
                    "image": image, "zigzag_direction": 1  # Adăugat pentru zigzag
                }

                if side == "top":
                    enemy_data.update({"x": random.randint(0, SCREEN_WIDTH), "y": -enemy_size, "dx": 0, "dy": speed})
                elif side == "bottom":
                    enemy_data.update({"x": random.randint(0, SCREEN_WIDTH), "y": SCREEN_HEIGHT + enemy_size, "dx": 0, "dy": -speed})
                elif side == "left":
                    enemy_data.update({"x": -enemy_size, "y": random.randint(0, SCREEN_HEIGHT), "dx": speed, "dy": 0})
                elif side == "right":
                    enemy_data.update({"x": SCREEN_WIDTH + enemy_size, "y": random.randint(0, SCREEN_HEIGHT), "dx": -speed, "dy": 0})

                enemies.append(enemy_data)
            spawn_timer = 0

        for enemy in enemies:
            if enemy["type"] == "zigzag":
                enemy["x"] += enemy["dx"] + enemy["zigzag_direction"] * 3
                enemy["y"] += enemy["dy"]

                if enemy["x"] <= 0 or enemy["x"] >= SCREEN_WIDTH - 75:
                    enemy["zigzag_direction"] *= -1
            else:
                enemy["x"] += enemy["dx"]
                enemy["y"] += enemy["dy"]

        for enemy in enemies:
            screen.blit(enemy["image"], (enemy["x"], enemy["y"]))

        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], 75, 75)
            if enemy["type"] == "runner":
                if player_rect.colliderect(enemy_rect):
                    lives -= 1
                    enemies.remove(enemy)
            elif enemy["type"] == "zigzag":
                if player_rect.colliderect(enemy_rect):
                    shield = 0
                    lives -= 1
                    enemies.remove(enemy)
            else:
                if player_rect.colliderect(enemy_rect):
                    if shield > 0:
                        shield -= 20
                    else:
                        lives -= 1
                    enemies.remove(enemy)

        enemies = [enemy for enemy in enemies if -enemy_size <= enemy["x"] <= SCREEN_WIDTH and -enemy_size <= enemy["y"] <= SCREEN_HEIGHT]

        if random.randint(1, powerup_spawn_chance) == 1:
            life_powerups.append({"x": random.randint(0, SCREEN_WIDTH - 30), "y": random.randint(0, SCREEN_HEIGHT - 30)})

        if random.randint(1, powerup_spawn_chance) == 1:
            destroy_all_powerups.append({"x": random.randint(0, SCREEN_WIDTH - 30), "y": random.randint(0, SCREEN_HEIGHT - 30)})

        for powerup in life_powerups[:]:
            powerup_rect = pygame.Rect(powerup["x"] - 15, powerup["y"] - 15, 30, 30)
            if player_rect.colliderect(powerup_rect):
                if lives < 3:  # Max 3 vieți
                    powerup_sound.play()
                    lives += 1
                life_powerups.remove(powerup)

        for powerup in destroy_all_powerups[:]:
            powerup_rect = pygame.Rect(powerup["x"], powerup["y"], 75, 75)
            if player_rect.colliderect(powerup_rect):
                destroy_powerup_sound.play()
                enemies.clear()  # Distruge toți inamicii de pe hartă
                destroy_all_powerups.remove(powerup)

        if lives <= 0:
            pygame.mixer.music.stop()
            save_to_leaderboard(score)
            show_game_over_message()
            main_menu()

        current_time = pygame.time.get_ticks()
        if current_time - last_score_update >= 1000:
            score += 1
            last_score_update = current_time

        if current_time - difficulty_timer >= 10000:
            enemy_speed += 0.2
            spawn_rate = max(40, spawn_rate - 3)
            difficulty_timer = current_time

        screen.blit(player_image, (square_x, square_y))
        for enemy in enemies:
            screen.blit(enemy["image"], (enemy["x"], enemy["y"]))
        for powerup in life_powerups:
            screen.blit(powerup_image, (powerup["x"], powerup["y"]))

        score_text = font.render(f"Score: {score}", True, text_color)
        screen.blit(score_text, (10, 10))

        for i in range(lives):
            screen.blit(heart_image, (10 + i * 40, 200))

        pygame.draw.rect(screen, (0, 255, 0), (10, 150, shield * 2, 20))
        pygame.draw.rect(screen, (255, 255, 255), (10, 150, 200, 20), 2)

        pygame.display.flip()
        pygame.time.Clock().tick(144)

main_menu()
