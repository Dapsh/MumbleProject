import pygame

# Создаем объект часов для управления FPS
clock = pygame.time.Clock()

# Инициализация Pygame и настройка окна
pygame.init()
screen = pygame.display.set_mode((618, 359))  # размеры экрана
pygame.display.set_caption("Mumble")  # заголовок окна
bg = pygame.image.load('BG.png').convert_alpha()  # загрузка фона

# Загружаем анимации для движения персонажа влево и вправо
walk_l = [
    pygame.image.load('Gotoleft/left1.png').convert_alpha(),
    pygame.image.load('Gotoleft/left2.png').convert_alpha(),
    pygame.image.load('Gotoleft/left3.png').convert_alpha(),
    pygame.image.load('Gotoleft/left4.png').convert_alpha(),
]
walk_r = [
    pygame.image.load('Gotorigth/right1.png').convert_alpha(),
    pygame.image.load('Gotorigth/right2.png').convert_alpha(),
    pygame.image.load('Gotorigth/right3.png').convert_alpha(),
    pygame.image.load('Gotorigth/right4.png').convert_alpha(),
]

# Загрузка изображения монстра и начальная координата его появления
ghost = pygame.image.load("Music/ghost.png").convert_alpha()
ghostx = 620  # координата появления монстра

# Список для хранения активных монстров
ghost_list = []

# Переменные для анимации, движения и других параметров игры
player_anim_count = 0  # счетчик кадров анимации персонажа
bgx = 0  # координата для циклической прокрутки фона
player_speed = 5  # скорость персонажа

# Начальные координаты персонажа
player_x = 150
player_y = 250

# Переменные для прыжка
is_jump = False  # флаг прыжка
jump_count = 8  # высота прыжка

# Загрузка фоновой музыки
bgs = pygame.mixer.Sound("Music/Fonbg.mp3")
bgs.play()

# Таймер для появления монстров
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)  # монстры появляются каждые 2.5 секунды

# Настройка шрифта и текста для проигрышного экрана
label = pygame.font.Font('Font/Arco.ttf', 40)
lose = label.render('Вы проиграли', False, (193, 196, 199))  # текст проигрыша
loser = label.render('Играть снова', False, (115, 132, 148))  # кнопка рестарта
restart_label = loser.get_rect(topleft=(180, 200))  # позиция кнопки рестарта

# Переменные игрового процесса
gameplay = True  # флаг, указывающий, идет ли игра
bullets_left = 5  # количество пуль
bullet = pygame.image.load("Music/bullet.png").convert_alpha()  # изображение пули
bullets = []  # список для хранения активных пуль

# Основной игровой цикл
running = True
while running:
    # Рисуем фон и его копию для эффекта движения
    screen.blit(bg, (bgx, 0))
    screen.blit(bg, (bgx + 618, 0))
    screen.blit(ghost, (ghostx, 250))  # рисуем монстра

    if gameplay:
        # Получаем список нажатых клавиш
        keys = pygame.key.get_pressed()

        # Получаем прямоугольник персонажа для проверки столкновений
        player_rect = walk_l[0].get_rect(topleft=(player_x, player_y))

        # Перебираем монстров на экране
        if ghost_list:
            for (i, el) in enumerate(ghost_list):
                screen.blit(ghost, el)  # рисуем монстра
                el.x -= 10  # двигаем монстра влево

                # Удаляем монстра, если он ушел за границу экрана
                if el.x < -10:
                    ghost_list.pop(i)

                # Проверяем столкновение персонажа с монстром
                if player_rect.colliderect(el):
                    gameplay = False  # если столкновение произошло, завершаем игру

        # Рисуем персонажа в зависимости от направления движения
        if keys[pygame.K_LEFT]:
            screen.blit(walk_l[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_r[player_anim_count], (player_x, player_y))

        # Обрабатываем движение персонажа влево и вправо
        if keys[pygame.K_LEFT] and player_x > 25:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        # Анимация движения персонажа
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        # Обрабатываем прыжок персонажа
        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        # Двигаем фон для создания эффекта движения
        bgx -= 2
        if bgx == -618:
            bgx = 0

        # Обрабатываем пули
        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))  # рисуем пулю
                el.x += 4  # пуля движется вправо

                # Удаляем пулю, если она ушла за границу экрана
                if el.x > 630:
                    bullets.pop(i)

                # Проверяем столкновение пуль с монстрами
                if ghost_list:
                    for (index, ghost_el) in enumerate(ghost_list):
                        if el.colliderect(ghost_el):
                            ghost_list.pop(index)  # удаляем монстра
                            bullets.pop(i)  # удаляем пулю

        # Двигаем монстра влево
        ghostx -= 10
    else:
        # Отображаем экран проигрыша
        screen.fill((87, 88, 89))  # заливаем экран серым цветом
        screen.blit(lose, (180, 100))  # текст проигрыша
        screen.blit(loser, restart_label)  # кнопка рестарта

        # Обрабатываем нажатие на кнопку рестарта
        mouse = pygame.mouse.get_pos()
        if restart_label.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True  # перезапускаем игру
            player_x = 150
            ghost_list.clear()  # очищаем список монстров
            bullets.clear()  # очищаем список пуль
            bullets_left = 5  # сбрасываем количество пуль

    # Обновляем экран
    pygame.display.update()

    # Обрабатываем события Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # обработка выхода из игры
            running = False
            pygame.quit()
        if event.type == ghost_timer:  # появление нового монстра
            ghost_list.append(ghost.get_rect(topleft=(620, 250)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            # Создаем новую пулю при нажатии пробела
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_left -= 1  # уменьшаем количество оставшихся пуль

    # Устанавливаем частоту обновления экрана
    clock.tick(14)
