from settings import *
from pygame.draw import rect as draw_rect
from resource_manager import ResourceManager


def draw_button_with_label(display_surface, button_text, label_text, font, y_pos):
    button_width = 200
    button_height = 50
    gap = 10
    label = font.render(label_text, True, "white")
    label_width = label.get_width()
    button_rect = pygame.Rect(
        WINDOW_WIDTH // 2 - button_width // 2, y_pos, button_width, button_height
    )
    display_label(
        display_surface,
        label_text,
        button_rect.x - label_width - gap,
        y_pos + (button_height - label.get_height()) // 2,
        font,
    )
    draw_rect(display_surface, "#895129", button_rect, border_radius=10)
    text_surf = font.render(button_text, True, "white")
    text_rect = text_surf.get_rect(center=button_rect.center)
    display_surface.blit(text_surf, text_rect.topleft)
    return button_rect


def draw_button(display_surface, text, font, y_pos, width=200, height=50):
    rect = pygame.Rect(WINDOW_WIDTH // 2 - width // 2, y_pos, width, height)
    draw_rect(display_surface, "#895129", rect, border_radius=10)
    text_surf = font.render(text, True, "white")
    text_rect = text_surf.get_rect(center=rect.center)
    display_surface.blit(text_surf, text_rect.topleft)
    return rect


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


def draw_music_volume_bar(display_surface, y_pos, font):
    volume = ResourceManager.get_music_volume()
    _draw_volume_bar(
        display_surface, y_pos, volume, "Music", font, ResourceManager.set_music_volume
    )


def draw_effects_volume_bar(display_surface, y_pos, font):
    volume = ResourceManager.get_effects_volume()
    _draw_volume_bar(
        display_surface,
        y_pos,
        volume,
        "Effects",
        font,
        ResourceManager.set_effects_volume,
    )


def _draw_volume_bar(display_surface, y_pos, volume, text, font, set_volume):
    X = WINDOW_WIDTH // 2
    WIDTH = 200
    HEIGHT = 20
    rect = pygame.Rect(X - WIDTH // 2, y_pos, WIDTH, HEIGHT)

    updated_volume = _update_volume_from_mouse(rect, volume, set_volume)
    _draw_bar(display_surface, rect, updated_volume)
    text_width = font.render(text, True, "white").get_width()
    display_label(display_surface, text, rect.x - text_width - 10, rect.y, font)


def _update_volume_from_mouse(rect, volume, set_volume):
    if not (
        pygame.mouse.get_pressed()[0] and rect.collidepoint(pygame.mouse.get_pos())
    ):
        return volume

    mouse_x = pygame.mouse.get_pos()[0]
    new_volume = max(0, min((mouse_x - rect.x) / rect.width, 1))

    set_volume(new_volume)

    return new_volume


def _draw_bar(display_surface, rect, volume):
    border_margin = 3
    smaller_rect = pygame.Rect(rect.x, rect.y, rect.width - border_margin, rect.height)
    draw_rect(display_surface, "white", smaller_rect, border_radius=10)
    draw_rect(
        display_surface,
        "#90D5FF",
        (rect.x, rect.y, volume * rect.width, rect.height),
        border_radius=10,
    )
