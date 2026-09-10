from ursina import *
from ursina.shaders import lit_with_shadows_shader
from random import uniform

from systems.database_loader import load_csv

class Skeleton(Entity):

    def __init__(self, position=(0, 1, 0)):

        super().__init__(
            parent=scene,
            model='quad',
            texture='resources/animations/skeleton/walk_1.png',
            scale=(5, 6, 1),
            position=position,
            billboard=True,
            collider='box',
            shader=lit_with_shadows_shader
        )

        self.walk_frames = [
            'resources/animations/skeleton/attack_1.png',
            'resources/animations/skeleton/attack_1.png'
        ]

        self.frame_index = 0
        self.animation_timer = 0

        from systems.database_loader import load_csv

        stats = load_csv("database/creatures/skeleton.csv")[0]

        self.health = int(stats["health"])
        self.damage = int(stats["damage"])
        self.speed = float(stats["speed"])
        
        self.target_position = Vec3(
            uniform(-25, 25),
            1.5,
            uniform(-25, 25)
        )
              

    def update(self):

        self.animate_walk()
        self.move_randomly()

    def animate_walk(self):

        self.animation_timer += time.dt

        if self.animation_timer >= 0.2:

            self.frame_index += 1

            if self.frame_index >= len(self.walk_frames):
                self.frame_index = 0

            self.texture = self.walk_frames[self.frame_index]

            self.animation_timer = 0

    def move_randomly(self):

        direction = self.target_position - self.position

        distance = direction.length()

        if distance > 0.1:

            direction = direction.normalized()

            self.position += direction * self.speed * time.dt

        else:

            self.pick_new_target()

        self.check_wall_collision()        

    def pick_new_target(self):

        self.target_position = Vec3(
            uniform(-25, 25),
            1.5,
            uniform(-25, 25)
        )    

    def check_wall_collision(self):

        limit = 32

        if self.x >= limit:
            self.pick_new_target()

        if self.x <= -limit:
            self.pick_new_target()

        if self.z >= limit:
            self.pick_new_target()

        if self.z <= -limit:
            self.pick_new_target()    