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
