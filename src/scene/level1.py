from scene.level import Level


class Level1(Level):
    def __init__(self, director):
        super().__init__(director, level="level1.tmx", remaining_lives=3,
                         background="background1", music="level_1.ogg")

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

        self._handle_player_collisions_with_enemies()

        self.hud.draw_hud(self.player.health_points, self.remaining_lives)
