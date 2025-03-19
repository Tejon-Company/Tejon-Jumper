from settings import *


def create_animation_rects(frame_start_x, number_of_frames, sprite_size):
    frame_start_x *= sprite_size
    y = 0
    pixel_gap = 1
    animation_rects = []

    for i in range(number_of_frames):
        x = (frame_start_x + frame_start_x//sprite_size) + \
            (sprite_size * i) + (i * pixel_gap)
        animation_rects.append((x, y, sprite_size, sprite_size))

    return animation_rects


def update_animation(delta_time, entity):
    _update_animation_frame(delta_time, entity)
    entity._update_sprite()


def _update_animation_frame(delta_time, entity):
    entity.animation_time += delta_time
    frames_in_animation = len(entity.animations)
    elapsed_frames = entity.animation_time / entity.animation_speed
    entity.animation_frame = int(elapsed_frames) % frames_in_animation


def setup_animation(entity):
    entity.animation_frame = 0
    entity.animation_speed = 0.2
    entity.animation_time = 0
