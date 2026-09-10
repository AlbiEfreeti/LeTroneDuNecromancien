from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
from creatures import skeleton
from creatures.skeleton import Skeleton


def build_level(necromancer, GamePlayer):

    room_entities = []

    floor = Entity(
        model='plane',
        scale=(70, 1, 70),
        texture='resources/images/floor_main.png',
        collider='box',
        shader=lit_with_shadows_shader
    )

    ceiling = Entity(
        model='plane',
        scale=(70, 1, 70),
        position=(0, 10, 0),
        rotation=(180, 0, 0),
        texture='resources/images/floor_main.png',
        collider='box',
        shader=lit_with_shadows_shader
    )

    wall_1 = Entity(
    model='cube',
    scale=(70, 12.2, 0.1),
    position=(0, 6, 35),
    texture='resources/images/final_wall.png',
    collider='box',
    shader=lit_with_shadows_shader
    )

    wall_2 = Entity(
        model='cube',
        scale=(70, 12.2, 0.1),
        position=(0, 6, -35),
        texture='resources/images/final_wall.png',
        collider='box',
        shader=lit_with_shadows_shader
    )

    wall_3 = Entity(
        model='cube',
        scale=(0.1, 12.2, 70),
        position=(35, 6, 0),
        texture='resources/images/final_wall.png',
        collider='box',
        shader=lit_with_shadows_shader
    )

    wall_4 = Entity(
        model='cube',
        scale=(0.1, 12.2, 70),
        position=(-35, 6, 0),
        texture='resources/images/final_wall.png',
        collider='box',
        shader=lit_with_shadows_shader
    )

    light = DirectionalLight(
    shadows=True
    )

    light.look_at(Vec3(1, -1, -1))

    ambient = AmbientLight(color=color.rgba(120, 120, 120, 0.6))

    Sky(color=color.rgb(100, 100, 120))

    player = GamePlayer(
        position=(0, 2, 0),
        speed=necromancer.speed,
        jump_height=2,
        gravity=1
    )

    player.cursor.visible = True
    mouse.locked = True

    fade = Entity(
    parent=camera.ui,
    model='quad',
    color=color.black,
    scale=(2, 2),
    z=-10
    )

    fade.animate_color(
        color.rgba(0, 0, 0, 0),
        duration=2
    )

    level1_text = Text(
        parent=camera.ui,
        text='LEVEL 1: THE FALLEN CRYPT',
        font='resources/fonts/MFCRegular.ttf',
        origin=(0, 4.5),
        scale=3,
        color=color.white,
        y=0.35,
        z=-9
    )

    level1_text.animate(
        'alpha',
        0,
        duration=5
    )

    destroy(level1_text, delay=3)
    destroy(fade, delay=2)

    room_entities.extend([
        floor,
        ceiling,
        wall_1,
        wall_2,
        wall_3,
        wall_4,
        light,
        ambient
    ])

    skeleton_1 = Skeleton(
        position=(10, 2, 10),
    )

    skeleton_2 = Skeleton(
        position=(-12, 2, 15),
    )

    skeleton_3 = Skeleton(
        position=(20, 2, -8),
    )

    skeleton_4 = Skeleton(
        position=(-18, 2, -20),
    )

    skeleton_1.enabled = False
    skeleton_2.enabled = False
    skeleton_3.enabled = False
    skeleton_4.enabled = False

    def spawn_skeleton(skeleton):

        skeleton.enabled = True

        Audio(
            'resources/audio/skeleton_appears.mp3',
            autoplay=True,
            pitch=1.15
        )


    invoke(spawn_skeleton, skeleton_1, delay=5)
    invoke(spawn_skeleton, skeleton_2, delay=5.5)
    invoke(spawn_skeleton, skeleton_3, delay=6)
    invoke(spawn_skeleton, skeleton_4, delay=6.5)

    room_entities.extend([
        skeleton_1,
        skeleton_2,
        skeleton_3,
        skeleton_4
    ])
    return player, room_entities