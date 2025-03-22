import pygame
from pygame.draw import rect as draw_rect
from resource_manager import ResourceManager


def draw_button(display_surface, rect, text, font):
    draw_rect(display_surface, "#895129", rect, border_radius=10)
    text_surf = font.render(text, True, "white")
    text_rect = text_surf.get_rect(center=rect.center)
    display_surface.blit(text_surf, text_rect.topleft)


def display_background(display_surface, background):
    display_surface.blit(background, (0, 0))


def display_label(display_surface, text, x, y, font):
    label = font.render(text, True, "white")
    padding = 4
    label_width = label.get_width() + padding * 2
    label_height = label.get_height() + padding * 2
    label_bg = pygame.Surface((label_width, label_height), pygame.SRCALPHA)
    rect = label_bg.get_rect()
    pygame.draw.rect(label_bg, "#9A7856", rect, border_radius=5)
    display_surface.blit(label_bg, (x - padding, y - padding))
    display_surface.blit(label, (x, y))


def draw_volume_bar(display_surface, rect, volume, text, font):
    volume = _update_volume_from_mouse(rect, volume, text)
    _draw_bar(display_surface, rect, volume)
    text_width = font.render(text, True, "white").get_width()
    display_label(display_surface, text, rect.x - text_width - 10, rect.y, font)


def _update_volume_from_mouse(rect, volume, text):
    if not (
        pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos())
    ):
        return volume

    mouse_x = pygame.mouse.get_pos()[0]
    new_volume = max(0, min((mouse_x - rect.x) / rect.width, 1))

    if text == "Music":
        ResourceManager.set_music_volume(new_volume)
    else:
        ResourceManager.set_effects_volume(new_volume)

    return new_volume


def _draw_bar(display_surface, rect, volume):
    draw_rect(display_surface, "white", rect, border_radius=10)
    draw_rect(
        display_surface,
        "#90D5FF",
        (rect.x, rect.y, volume * rect.width, rect.height),
        border_radius=10,
    )
