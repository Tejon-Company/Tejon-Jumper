from scene.level import Level
from settings import *
from characters.sprite import Sprite


class Level2(Level):
    def __init__(self, director):
        super().__init__(director, level="level2.tmx", remaining_lives=3,
                         background="background1", music="level_1.ogg")
        self._setup_shadow()

    def _setup_shadow(self):
        for x, y, surf in self.tmx_map.get_layer_by_name("Shadow").tiles():
            Sprite(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                (self.groups["shadow"]),
            )
        
    def draw(self, display_surface):
        self.camera.draw_background(
            self.groups["backgrounds"], display_surface)

        for sprite in self.groups["deco"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for sprite in self.groups["all_sprites"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        for projectile in self.groups["projectiles"]:
            if projectile.is_activated:
                display_surface.blit(
                    projectile.image, self.camera.apply(projectile))

        for sprite in self.groups["berries"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))
            
        for sprite in self.groups["shadow"]:
            shadow_layer = self.tmx_map.get_layer_by_name("Shadow")
            opacity = int(shadow_layer.opacity * 255)
            shadow_image = sprite.image.copy()
            shadow_image.set_alpha(opacity)
            display_surface.blit(shadow_image, self.camera.apply(sprite))

        self._handle_player_collisions()

        self.hud.draw_hud(self.player.health_points, self.remaining_lives)
