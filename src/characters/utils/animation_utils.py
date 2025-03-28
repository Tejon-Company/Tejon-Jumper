from singletons.settings.resolution_settings import ResolutionSettings


def create_animation_rects(
    frame_start_x, number_of_frames, sprite_width=None, sprite_height=None
):
    resolution_settings = ResolutionSettings()
    sprite_width = sprite_width or resolution_settings.tile_size
    sprite_height = sprite_height or resolution_settings.tile_size

    start_pixel = frame_start_x * sprite_width
    offset = start_pixel + start_pixel // sprite_width
    pixel_gap = 1
    step = sprite_width + pixel_gap
    y = 0

    def calculate_rect(i):
        x = offset + (i * step)
        return x, y, sprite_width, sprite_height

    return [calculate_rect(i) for i in range(number_of_frames)]


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
