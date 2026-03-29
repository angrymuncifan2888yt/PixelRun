import pygame


def player_input(player, delta, mouse=True):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
        player.jump()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left(delta)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right(delta)

    if mouse:
        mouse2 = pygame.mouse.get_pressed()
        if mouse2[0]:
            player.jump()


def player_click(player, event, mouse=True):
    if event.type == pygame.KEYDOWN:
        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            player.is_clicking = True
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if mouse:
            player.is_clicking = True