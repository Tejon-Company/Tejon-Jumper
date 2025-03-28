from pygame.draw import rect as draw_rect
from pygame.rect import Rect
from resource_manager import ResourceManager
from singletons.settings.resolution_settings import ResolutionSettings
import pygame


def check_if_button_was_clicked(button, pos):
    """
    Comprueba si un botón fue clickeado y reproduce un sonido si es así.

    Args:
        button: Objeto Rect que representa el botón.
        pos: Tupla (x, y) con la posición del clic.

    Returns:
        bool: True si el botón fue clickeado, False en caso contrario.
    """
    click_button_sound = ResourceManager.load_sound_effect("click_button.ogg")

    if button.collidepoint(pos):
        click_button_sound.play()
        return True

    return False


def draw_button_with_label(display_surface, button_text, label_text, font, y_pos):
    """
    Dibuja un botón con una etiqueta a su izquierda.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        button_text: Texto que se mostrará en el botón.
        label_text: Texto que se mostrará en la etiqueta.
        font: Fuente para renderizar los textos.
        y_pos: Posición vertical del botón.

    Returns:
        Rect: Rectángulo que representa el botón dibujado.
    """
    resolution_settings = ResolutionSettings()
    gap = int(resolution_settings.window_width * 0.01)
    button_rect = draw_button(display_surface, button_text, font, y_pos)

    label_surface = font.render(label_text, True, "white")
    label_width = label_surface.get_width()
    label_height = label_surface.get_height()
    label_y = y_pos + (button_rect.height - label_height) // 2
    label_x = button_rect.x - label_width - gap
    display_label(display_surface, label_text, label_x, label_y, font)

    return button_rect


def display_label(display_surface, text, x, y, font):
    """
    Muestra una etiqueta de texto con fondo en la pantalla.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        text: Texto a mostrar en la etiqueta.
        x: Posición horizontal de la etiqueta.
        y: Posición vertical de la etiqueta.
        font: Fuente para renderizar el texto.
    """
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
    """
    Dibuja un rectángulo con bordes redondeados en la pantalla.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        rect: Objeto Rect que define el rectángulo.
        background_color: Color del rectángulo.
        border_radius: Radio de las esquinas redondeadas. Por defecto es 10.
    """
    draw_rect(display_surface, background_color, rect, border_radius=border_radius)


def draw_button(display_surface, text, font, y_pos, width=None, height=None):
    """
    Dibuja un botón en la pantalla.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        text: Texto a mostrar en el botón.
        font: Fuente para renderizar el texto.
        y_pos: Posición vertical del botón.
        width: Ancho del botón. Si es None, se usa un valor proporcional a la ventana.
        height: Alto del botón. Si es None, se usa un valor proporcional a la ventana.

    Returns:
        Rect: Rectángulo que representa el botón dibujado.
    """
    settings = ResolutionSettings()
    width, height = _get_button_dimensions(width, height)
    button_rect = Rect(settings.window_width // 2 - width // 2, y_pos, width, height)
    brown = "#895129"
    _draw_background_rect(display_surface, button_rect, brown)
    _draw_button_text(display_surface, text, button_rect, font)
    return button_rect


def _get_button_dimensions(width, height):
    """
    Calcula las dimensiones de un botón basándose en el tamaño de la ventana.

    Args:
        width: Ancho especificado. Si es None, se calcula automáticamente.
        height: Alto especificado. Si es None, se calcula automáticamente.

    Returns:
        tuple: (width, height) con las dimensiones del botón.
    """
    settings = ResolutionSettings()
    if width is None:
        width = int(settings.window_width * 0.2)
    if height is None:
        height = int(settings.window_height * 0.07)
    return width, height


def _draw_button_text(display_surface, text, rect, font):
    """
    Dibuja el texto de un botón centrado en su rectángulo.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        text: Texto a mostrar en el botón.
        rect: Rectángulo del botón donde se centrará el texto.
        font: Fuente para renderizar el texto.
    """
    text_surface = font.render(text, True, "white")
    text_rect = text_surface.get_rect(center=rect.center)
    display_surface.blit(text_surface, text_rect.topleft)


def draw_background(display_surface, background=None):
    """
    Dibuja el fondo del menú en la superficie de visualización.

    Args:
        display_surface: Superficie de pygame donde dibujar el fondo.
        background: Imagen de fondo opcional. Si es None, se carga la imagen predeterminada.
    """
    background = ResourceManager.load_image("menu_background.jpeg")
    display_surface.blit(background, (0, 0))


def draw_music_volume_bar(display_surface, y_pos, font):
    """
    Dibuja una barra de ajuste para el volumen de la música.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        y_pos: Posición vertical de la barra.
        font: Fuente para renderizar el texto.
    """
    volume = ResourceManager.get_music_volume()
    _draw_volume_bar(
        display_surface, y_pos, volume, "Música", font, ResourceManager.set_music_volume
    )


def draw_effects_volume_bar(display_surface, y_pos, font):
    """
    Dibuja una barra de ajuste para el volumen de los efectos de sonido.

    Args:
        display_surface: Superficie de pygame donde dibujar.
        y_pos: Posición vertical de la barra.
        font: Fuente para renderizar el texto.
    """
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
    """
     Dibuja una barra de volumen interactiva en la posición vertical especificada.

    Args:
        display_surface: Superficie donde se dibujará la barra.
        y_pos: Posición vertical de la barra en la pantalla.
        volume: Valor actual del volumen (entre 0.0 y 1.0).
        text: Texto descriptivo para mostrar junto a la barra.
        font: Fuente utilizada para renderizar el texto.
        set_volume: Función para establecer el nuevo volumen cuando se modifica.
    """
    settings = ResolutionSettings()
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
    """
    Actualiza el volumen basado en la interacción del ratón con la barra de volumen.

    Args:
        rect: Rectángulo que define el área de la barra de volumen.
        set_volume: Función para establecer el volumen en el sistema.

    Returns:
        float: El valor actualizado del volumen (si hubo cambio) o el valor original.
    """
    mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_over_volume_bar = rect.collidepoint(pygame.mouse.get_pos())

    if not (mouse_pressed and mouse_over_volume_bar):
        return volume

    mouse_x = pygame.mouse.get_pos()[0]
    new_volume = max(0, min((mouse_x - rect.x) / rect.width, 1))

    set_volume(new_volume)

    return new_volume


def _draw_bar(display_surface, rect, volume):
    """
    Dibuja una barra de volumen en la pantalla.

    Args:
        display_surface: Superficie de pygame donde se dibujará la barra.
        rect: Objeto Rect que define la posición y dimensiones de la barra.
        volume: Valor entre 0 y 1 que representa el nivel de volumen a mostrar.
    """
    settings = ResolutionSettings()
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
