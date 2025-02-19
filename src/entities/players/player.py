from settings import *
from entities.character import Character


class Player(Character):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)

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

        self.on_surface = False

    def update(self, platform_rects, delta_time):
        self.old_rect = self.rect.copy()
        self._input()
        self._move(platform_rects, delta_time)
        self._detect_platform_contact(platform_rects)

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

    def _move(self, platform_rects, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self._collision("horizontal", platform_rects)

        self.rect.y += self.fall * delta_time
        self.fall += self.gravity / 2 * delta_time
        self._collision("vertical", platform_rects)

        if self.jump:
            if self.on_surface:
                self.fall = -self.jump_height

            self.direction.y = 0
            self._normalize_direction()
            self.jump = False

    def _collision(self, axis, platform_rects):
        for platform_rect in platform_rects:
            if not platform_rect.colliderect(self.rect):
                continue

            if axis == "horizontal":
                self._handle_horizontal_collision(platform_rect)
            else:
                self._handle_vertical_collision(platform_rect)

    def _handle_horizontal_collision(self, platform_rect):
        self._handle_right_collission(platform_rect)
        self._handle_left_collision(platform_rect)

    def _handle_right_collission(self, platform_rect):
        approaching_from_left = self.rect.right >= platform_rect.left
        player_was_on_left = self.old_rect.right <= platform_rect.left
        is_right_collision = approaching_from_left and player_was_on_left

        if is_right_collision:
            self.rect.right = platform_rect.left

    def _handle_left_collision(self, platform_rect):
        approaching_from_right = self.rect.left <= platform_rect.right
        player_was_on_right = self.old_rect.left >= platform_rect.right
        is_left_collision = approaching_from_right and player_was_on_right

        if is_left_collision:
            self.rect.left = platform_rect.right

    def _handle_vertical_collision(self, platform_rect):
        self._handle_bottom_collision(platform_rect)
        self._handle_top_collision(platform_rect)

        self.direction.y = 0

    def _handle_bottom_collision(self, platform_rect):
        approaching_from_top = self.rect.bottom >= platform_rect.top
        was_above = self.old_rect.bottom <= platform_rect.top
        is_bottom_collision = approaching_from_top and was_above

        if is_bottom_collision:
            self.rect.bottom = platform_rect.top

    def _handle_top_collision(self, platform_rect):
        approaching_from_bottom = self.rect.top <= platform_rect.bottom
        was_below = self.old_rect.top >= platform_rect.bottom
        is_top_collision = approaching_from_bottom and was_below

        if is_top_collision:
            self.rect.top = platform_rect.bottom

    def _detect_platform_contact(self, platform_rects):
        character_height = 2
        platform_rect = pygame.Rect(
            self.rect.bottomleft, (self.rect.width, character_height)
        )

        self.on_surface = platform_rect.collidelist(platform_rects) >= 0
