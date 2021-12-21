import pygame
from random import randrange

# Координаты поля
RES = 800
SIZE = 50

# Задаем рандомные положения змейки и яблок.
x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)

length = 1  # Длина
snake = [(x, y)]  # Положение
dx, dy = 0, 0  # Направления движения
fps = 60  # Скорость
dirs = {'W': True, 'S': True, 'A': True, 'D': True, }
# Объявляем счетчик рекорда.
score = 0
speed_count, snake_speed = 0, 10

# Инициализируем модуль pygame
pygame.init()
# Создание рабочего окна
surface = pygame.display.set_mode([RES, RES])
# Регулирование скорости
clock = pygame.time.Clock()
# Установка шрифта.
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)


# Закрытие игрыв
def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


# Суть змейки будет заключаться в следующем, на каждой итерации прохождения
# Змейки по квадрату, наш квадрат закрашивается, кроме самой змейки.
while True:
    surface.fill(pygame.Color('black'))
    # Рисуем змейку и яблоко, отображение секций змейки.
    [pygame.draw.rect(surface, pygame.Color('green'), (i, j, SIZE - 1, SIZE - 1)) for i, j in snake]
    pygame.draw.rect(surface, pygame.Color('red'), (*apple, SIZE, SIZE))
    # Рекорд
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
    surface.blit(render_score, (5, 5))
    # Изначально змейка представлена ввиде квадрата, на каждой следующей
    # итерации змейка увеличивается на 1 квадрат.
    speed_count += 1
    if not speed_count % snake_speed:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        # Срез координат, для того, чтобы змейка небыла непрерывной.
        snake = snake[-length:]
    # Поедание яблока. Работает так: когда положение координат= положению яблока
    # Это будет означать, что мы его съели.
    if snake[-1] == apple:
        apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
        # Увеличиваем длину и скорость змейки.
        length += 1
        score += 1
        snake_speed -= 1
        snake_speed = max(snake_speed, 4)
    # Конец игры, когда змейка вышла за пределы поля или когда съели себя.
    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        while True:
            render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
            surface.blit(render_end, (RES // 2 - 200, RES // 3))
            pygame.display.flip()
            close_game()

    # Обновляем задержку, обновляем fps
    pygame.display.flip()
    clock.tick(fps)
    close_game()
    # Управление. Под каждую кнопку прописываем свои координаты.
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True, }
    elif key[pygame.K_s]:
        if dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True, }
    elif key[pygame.K_a]:
        if dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False, }
    elif key[pygame.K_d]:
        if dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True, }
