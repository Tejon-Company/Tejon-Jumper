from singletons.settings import Settings


def create_animation_rects(
    frame_start_x, number_of_frames, sprite_width=None, sprite_height=None
):
    settings = Settings()
    if sprite_width is None:
        sprite_width = settings.tile_size

    if sprite_height is None:
        sprite_height = settings.tile_size

    frame_start_x *= sprite_width
    y = 0
    pixel_gap = 1
    animation_rects = []

    for i in range(number_of_frames):
        x = (
            (frame_start_x + frame_start_x // sprite_width)
            + (sprite_width * i)
            + (i * pixel_gap)
        )
        animation_rects.append((x, y, sprite_width, sprite_height))

    return animation_rects


def set_animation_parameters(entity):
    entity.animation_frame = 0
    entity.animation_speed = 0.2
    entity.animation_time = 0


def update_animation(delta_time, entity, animations):
    _update_animation_frame(delta_time, entity, animations)
    entity.update_sprite()


def _update_animation_frame(delta_time, entity, animations):
    entity.animation_time += delta_time
    frames_in_animation = len(animations)
    elapsed_frames = entity.animation_time / entity.animation_speed
    entity.animation_frame = int(elapsed_frames) % frames_in_animation
