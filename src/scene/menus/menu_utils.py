from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from resource_manager import ResourceManager
from singletons.settings import Settings
import pygame


def draw_button_with_label(display_surface, button_text, label_text, font, y_pos):
    settings = Settings()
    gap = int(settings.window_width * 0.01)
    button_rect = draw_button(display_surface, button_text, font, y_pos)

    label_surface = font.render(label_text, True, "white")
    label_width = label_surface.get_width()
    label_height = label_surface.get_height()
    label_y = y_pos + (button_rect.height - label_height) // 2
    label_x = button_rect.x - label_width - gap
    display_label(display_surface, label_text, label_x, label_y, font)

    return button_rect


def display_label(display_surface, text, x, y, font):
    padding = 4
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(topleft=(x, y))
    label_rect = Rect(
        x - padding,
        y - padding,
        text_rect.width + padding * 2,
        text_rect.height + padding * 2,
    )
    brown = "#9A7856"
    _draw_background_rect(display_surface, label_rect, brown, border_radius=5)
    display_surface.blit(text_surface, (x, y))


def _draw_background_rect(display_surface, rect, background_color, border_radius=10):
    draw_rect(display_surface, background_color, rect, border_radius=border_radius)


def draw_button(display_surface, text, font, y_pos, width=None, height=None):
    settings = Settings()
    width, height = _get_button_dimensions(width, height)
    button_rect = Rect(settings.window_width // 2 - width // 2, y_pos, width, height)
    brown = "#895129"
    _draw_background_rect(display_surface, button_rect, brown)
    _draw_button_text(display_surface, text, button_rect, font)
    return button_rect


def _get_button_dimensions(width, height):
    settings = Settings()
    if width is None:
        width = int(settings.window_width * 0.2)
    if height is None:
        height = int(settings.window_height * 0.07)
    return width, height


def _draw_button_text(display_surface, text, rect, font):
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(center=rect.center)
    display_surface.blit(text_surface, text_rect.topleft)


def draw_background(display_surface, background):
    display_surface.blit(background, (0, 0))


def draw_music_volume_bar(display_surface, y_pos, font):
    volume = ResourceManager.get_music_volume()
    _draw_volume_bar(
        display_surface, y_pos, volume, "Música", font, ResourceManager.set_music_volume
    )


def draw_effects_volume_bar(display_surface, y_pos, font):
    volume = ResourceManager.get_effects_volume()
    _draw_volume_bar(
        display_surface,
        y_pos,
        volume,
        "Efectos de sonido",
        font,
        ResourceManager.set_effects_volume,
    )


def _draw_volume_bar(display_surface, y_pos, volume, text, font, set_volume):
    settings = Settings()
    center_x = settings.window_width // 2
    bar_width = settings.window_width * 0.2
    bar_height = settings.window_height * 0.03
    rect = Rect(center_x - bar_width // 2, y_pos, bar_width, bar_height)

    updated_volume = _update_volume_from_mouse(rect, volume, set_volume)
    _draw_bar(display_surface, rect, updated_volume)
    text_width = font.render(text, True, "white").get_width()
    label_offset = int(settings.window_width * 0.01)
    display_label(
        display_surface, text, rect.x - text_width - label_offset, rect.y, font
    )


def _update_volume_from_mouse(rect, volume, set_volume):
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_over_volume_bar = rect.collidepoint(pygame.mouse.get_pos())

    if not (mouse_pressed and mouse_over_volume_bar):
        return volume

    mouse_x = pygame.mouse.get_pos()[0]
    new_volume = max(0, min((mouse_x - rect.x) / rect.width, 1))

    set_volume(new_volume)

    return new_volume


def _draw_bar(display_surface, rect, volume):
    settings = Settings()
    border_margin = settings.window_width * 0.005
    smaller_rect = Rect(rect.x, rect.y, rect.width - border_margin, rect.height)
    _draw_background_rect(display_surface, smaller_rect, "white", border_radius=10)

    blue = "#90D5FF"
    draw_rect(
        display_surface,
        blue,
        (rect.x, rect.y, volume * rect.width, rect.height),
        border_radius=10,
    )
