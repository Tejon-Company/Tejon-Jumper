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
        self.gravity = 500
        self.jump = False
        self.jump_height = 300

        self.collision_sprites = collision_sprites
        self.on_surface = False

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)

        if keys[pygame.K_RIGHT]:
            input_vector.x += 1

        if keys[pygame.K_LEFT]:
            input_vector.x -= 1

        if input_vector:
            self.direction.x = input_vector.normalize().x
        else:
            self.direction.x = input_vector.x

        if keys[pygame.K_SPACE]:
            self.jump = True

    def move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision("horizontal")

        self.direction.y += self.gravity / 2 * delta_time
        self.rect.y += self.direction.y * delta_time
        self.direction.y += self.gravity / 2 * delta_time
        self.collision("vertical")

        if self.jump:
            if self.on_surface:
                self.direction.y = -self.jump_height

            self.jump = False

    def check_contact(self):
        player_height = 2
        floor_rect = pygame.Rect(self.rect.bottomleft, (self.rect.width, player_height))
        collide_rects = [sprite.rect for sprite in self.collision_sprites]

        if floor_rect.collidelist(collide_rects) >= 0:
            self.on_surface = True
        else:
            self.on_surface = False

    def collision(self, axis):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if axis == "horizontal":
                    # left
                    if (
                        self.rect.left <= sprite.rect.right
                        and self.old_rect.left >= sprite.old_rect.right
                    ):
                        self.rect.left = sprite.rect.right

                    # right
                    if (
                        self.rect.right >= sprite.rect.left
                        and self.old_rect.right <= sprite.old_rect.left
                    ):
                        self.rect.right = sprite.rect.left
                else:  # vertical
                    # top
                    if (
                        self.rect.top <= sprite.rect.bottom
                        and self.old_rect.top >= sprite.old_rect.bottom
                    ):
                        self.rect.top = sprite.rect.bottom

                    # bottom
                    if (
                        self.rect.bottom >= sprite.rect.top
                        and self.old_rect.bottom <= sprite.old_rect.top
                    ):
                        self.rect.bottom = sprite.rect.top

                    # cancel gravity if there is a vertical collission
                    self.direction.y = 0

    def update(self, delta_time):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(delta_time)
        self.check_contact()
