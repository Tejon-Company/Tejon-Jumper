def create_animation_rects(start_x, y, width, height, frames, pixel_gap):
    animation_rects = []
    for i in range(frames):
        x = (start_x + start_x//32) + (width * i) + (i * pixel_gap)
        animation_rects.append((x, y, width, height))
    return animation_rects
