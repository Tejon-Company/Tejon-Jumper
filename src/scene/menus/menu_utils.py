from pygame.draw import rect as draw_rect


def draw_button(display_surface, rect, text, font):
    draw_rect(display_surface, "#895129", rect, border_radius=10)
    text_surf = font.render(text, True, "white")
    text_rect = text_surf.get_rect(center=rect.center)
    display_surface.blit(text_surf, text_rect.topleft)


def display_background(display_surface, background):
    display_surface.blit(background, (0, 0))
