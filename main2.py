import pygame
import random
import sys
from tkinter import messagebox

# Инициализация pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
PINK = (255, 182, 193)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
HOVER_COLOR = (200, 200, 200)

# Настройки экрана
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')

# FPS контроллер
clock = pygame.time.Clock()
INITIAL_FPS = 8  # Начальная скорость

# Создаем простые поверхности вместо изображений
background_img = pygame.Surface((WIDTH, HEIGHT))
background_img.fill(BLACK)

snake_head_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
snake_body_img = pygame.Surface((CELL_SIZE, CELL_SIZE))

food_img = pygame.Surface((CELL_SIZE, CELL_SIZE))
food_img.fill(RED)

# Функция отображения текста
def show_text(text, font_size, color, position):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Функция для создания кнопок
def create_button(text, font_size, color, rect, hover_color, mouse_pos):
    pygame.draw.rect(screen, hover_color if rect.collidepoint(mouse_pos) else color, rect)
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))

# Функция для показа красивого окна ошибки
def show_error_message():
    error_window_width = 400
    error_window_height = 200
    error_window = pygame.Surface((error_window_width, error_window_height))
    error_window.fill(BLACK)  # Черный фон окна ошибки

    # Рамка окна ошибки
    pygame.draw.rect(error_window, WHITE, error_window.get_rect(), 5)

    # Текст в центре окна
    font = pygame.font.SysFont(None, 40)
    error_text = font.render("Ошибка", True, WHITE)
    error_message = font.render("Цвет недоступен!", True, WHITE)

    # Центрируем текст
    text_rect = error_text.get_rect(center=(error_window_width // 2, 50))
    message_rect = error_message.get_rect(center=(error_window_width // 2, 120))

    # Отображаем текст
    error_window.blit(error_text, text_rect)
    error_window.blit(error_message, message_rect)

    # Отображение окна ошибки на экране
    screen.blit(error_window, ((WIDTH - error_window_width) // 2, (HEIGHT - error_window_height) // 2))

    pygame.display.flip()
    pygame.time.wait(3000)  # Ожидание 3 секунды

# Меню настроек
def settings_menu():
    global WIDTH, HEIGHT, CELL_SIZE, INITIAL_FPS, snake_head_img, snake_body_img

    running = True
    selected_speed = 8
    selected_color = PINK
    color_error = False  # Флаг для проверки ошибки выбора цвета

    green_button_rect = pygame.Rect(50, 250, 200, 50)
    blue_button_rect = pygame.Rect(50, 320, 200, 50)
    pink_button_rect = pygame.Rect(50, 390, 200, 50)
    apply_button_rect = pygame.Rect(WIDTH // 2 - 100, 500, 200, 50)

    while running:
        screen.fill(BLACK)
        mouse_pos = pygame.mouse.get_pos()

        # Текст
        show_text("Настройки", 50, WHITE, (WIDTH // 2 - 100, 50))
        show_text(f"Скорость змейки: {selected_speed}", 35, WHITE, (50, 150))

        # Кнопки выбора цвета
        create_button("1. Зеленый", 35, GREEN, green_button_rect, HOVER_COLOR, mouse_pos)
        create_button("2. Синий", 35, BLUE, blue_button_rect, HOVER_COLOR, mouse_pos)
        create_button("3. Розовый", 35, PINK, pink_button_rect, HOVER_COLOR, mouse_pos)

        # Кнопка принятия настроек
        create_button("Применить", 35, WHITE, apply_button_rect, HOVER_COLOR, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected_speed < 15:
                        selected_speed += 1
                elif event.key == pygame.K_DOWN:
                    if selected_speed > 1:
                        selected_speed -= 1
                elif event.key == pygame.K_RETURN:  # Нажатие на клавишу Enter
                    if color_error:
                        show_error_message()  # Показываем сообщение об ошибке
                    else:
                        INITIAL_FPS = selected_speed
                        snake_head_img.fill(selected_color)
                        snake_body_img.fill(selected_color)
                        running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Обработка нажатия на кнопки выбора цвета
                if green_button_rect.collidepoint(mouse_pos):
                    selected_color = GREEN
                    color_error = False
                elif blue_button_rect.collidepoint(mouse_pos):
                    selected_color = BLUE
                    color_error = False
                elif pink_button_rect.collidepoint(mouse_pos):
                    selected_color = PINK
                    color_error = False

                # Обработка нажатия кнопки "Применить"
                if apply_button_rect.collidepoint(mouse_pos):
                    if color_error:
                        show_error_message()
                    else:
                        INITIAL_FPS = selected_speed
                        snake_head_img.fill(selected_color)
                        snake_body_img.fill(selected_color)
                        running = False

        pygame.display.flip()
        clock.tick(30)

# Функция генерации еды
def generate_food():

    return (random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE)

# Функция отображения змейки
def draw_objects(snake, food, score):
    screen.blit(background_img, (0, 0))
    for index, segment in enumerate(snake):
        if index == 0:
            screen.blit(snake_head_img, segment)
        else:
            screen.blit(snake_body_img, segment)
    screen.blit(food_img, food)
    show_text(f'Score: {score}', 35, WHITE, (10, 10))
    pygame.display.flip()

# Функция отображения экрана окончания игры
def game_over_screen(score):
    screen.blit(background_img, (0, 0))
    show_text('Game Over', 75, RED, (WIDTH // 2 - 150, HEIGHT // 3))
    show_text(f'Score: {score}', 50, WHITE, (WIDTH // 2 - 70, HEIGHT // 2))
    # with open('rec.txt', 'w') as f:
    #     if f.read(1):
    #         if int(f.readline()) < score:
    #             messagebox.showinfo('Ура!', 'Вы поставили рекорд')
    #             f.clear()
    #             f.write(score)
    #     else: print("Fail pustoi")

    pygame.display.flip()
    pygame.time.delay(3000)

# Функция инициализации игры
def initialize_game():
    global snake, direction, food, score
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = 'UP'
    food = generate_food()  # Генерация еды
    score = 0
    return INITIAL_FPS

# Основной игровой цикл
def game_loop():
    global direction, food, score, snake

    current_fps = initialize_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        head_x, head_y = snake[0]
        if direction == 'UP':
            head_y -= CELL_SIZE
        elif direction == 'DOWN':
            head_y += CELL_SIZE
        elif direction == 'LEFT':
            head_x -= CELL_SIZE
        elif direction == 'RIGHT':
            head_x += CELL_SIZE

        new_head = (head_x, head_y)

        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT) or (new_head in snake):
            game_over_screen(score)
            current_fps = initialize_game()
            continue

        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            food = generate_food()  # Генерация новой еды
            if score % 10 == 0:
                current_fps += 1
        else:
            snake.pop()

        draw_objects(snake, food, score)
        clock.tick(current_fps)
# merge to master
# kjdhfgkjdhgksjl

if __name__ == "__main__":
    settings_menu()  # Отображение меню настроек перед началом игры
    game_loop()














































#if random.randint(0, 10) == 0:  # С вероятностью 1 к 10 еда появится за пределами поля
        #return (random.randrange(WIDTH, WIDTH + 100), random.randrange(HEIGHT, HEIGHT + 100))