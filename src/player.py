from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill("red")

        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()

        self.direction = vector(0, 0)
        self.speed = 150
        self.gravity = 1000
        self.fall = 0
        self.jump = False
        self.jump_height = 300

        self.collision_sprites = collision_sprites
        self.on_surface = False

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self._input()
        self._move(delta_time)
        self._check_contact()

    def _input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.jump = True

        self._normalize_direction()

    def _normalize_direction(self):
        if self.direction:
            self.direction = self.direction.normalize()

    def _move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self._collision("horizontal")

        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
        self._collision("vertical")

        if self.jump:
            if self.on_surface:
                self.fall = -self.jump_height

            self.direction.y = 0
            self._normalize_direction()
            self.jump = False

    def _check_contact(self):
        player_height = 2
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, player_height))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        self.on_surface = floor_rect.collidelist(collide_rects) >= 0

    def _collision(self, axis):
        for sprite in self.collision_sprites:
            if not sprite.rect.colliderect(self.rect):
                continue

            if axis == "horizontal":
                self._handle_horizontal_collision(sprite)
            else:
                self._handle_vertical_collision(sprite)

    def _handle_horizontal_collision(self, sprite):
        self._handle_right_collission(sprite)
        self._handle_left_collision(sprite)

    def _handle_right_collission(self, sprite):
        approaching_from_left = self.rect.right >= sprite.rect.left
        player_was_on_left = self.old_rect.right <= sprite.old_rect.left
        is_right_collision = approaching_from_left and player_was_on_left

        if is_right_collision:
            self.rect.right = sprite.rect.left

    def _handle_left_collision(self, sprite):
        approaching_from_right = self.rect.left <= sprite.rect.right
        player_was_on_right = self.old_rect.left >= sprite.old_rect.right
        is_left_collision = approaching_from_right and player_was_on_right

        if is_left_collision:
            self.rect.left = sprite.rect.right

    def _handle_vertical_collision(self, sprite):
        approaching_from_bottom = self.rect.top <= sprite.rect.bottom
        was_below = self.old_rect.top >= sprite.old_rect.bottom
        is_top_collision = approaching_from_bottom and was_below

        approaching_from_top = self.rect.bottom >= sprite.rect.top
        was_above = self.old_rect.bottom <= sprite.old_rect.top
        is_bottom_collision = approaching_from_top and was_above

        if is_top_collision:
            self.rect.top = sprite.rect.bottom
        if is_bottom_collision:
            self.rect.bottom = sprite.rect.top

        self.direction.y = 0
