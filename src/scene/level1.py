from scene.game_over import GameOver
from scene.level import Level
from scene.level2 import Level2


class Level1(Level):
    def __init__(self, director, remaining_lives=3, health_points=5):
        super().__init__(director, remaining_lives, health_points, level="level1.tmx",
                         background="background1", music_file="level_1.ogg")

    def handle_dead(self):
        self.director.pop_scene()
        if self.remaining_lives <= 0:
            self.director.stack_scene(GameOver(self.director))
        else:
            self.director.stack_scene(
                Level1(self.director, self.remaining_lives-1))

    def change_level(self):
        self.director.pop_scene()
        self.director.stack_scene(
            Level2(self.director, self.remaining_lives, self.player.health_points))

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

        for sprite in self.groups["flag"]:
            display_surface.blit(sprite.image, self.camera.apply(sprite))

        self._handle_player_collisions()

        self.hud.draw_hud(self.player.health_points, self.remaining_lives)
