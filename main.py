from levels.level_1 import build_level
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from systems.inventory import toggle_inventory
from systems.intro import start_intro
from systems.settings import open_settings
import csv
import os


app = Ursina()


menu_music = Audio(
    'resources/audio/Crypt_of_Ash.mp3',
    loop=True,
    autoplay=False
)

window.title = 'Necromancer Level Up'
window.borderless = True
window.fullscreen = True
window.exit_button.visible = True
window.fps_counter.enabled = True
window.exit_button.visible = False

Text.default_font = 'resources/fonts/MFCRegular.ttf'

player = None
room_entities = []
menu_entities = []
current_level = 1
game_paused = False
pause_menu_entities = []
in_game = False


from systems.database_loader import load_csv


class Necromancer:

    def __init__(self):

        data = load_csv("database/player/player.csv")[0]

        self.level = int(data["level"])
        self.health = int(data["health"])
        self.mana = int(data["mana"])
        self.damage = int(data["damage"])
        self.defense = int(data["defense"])
        self.speed = float(data["speed"])
        self.experience = int(data["experience"])


necromancer = Necromancer()


class GamePlayer(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.attack_cooldown = 0

        self.walk_sound = Audio(
                'resources/audio/footsteps_player.wav',
                autoplay=False,
                loop=True,
                volume=1,
                pitch=1.0
            )
    
    def update(self):
        super().update()

        if self.attack_cooldown > 0:
            self.attack_cooldown -= time.dt

        if held_keys['left mouse']:
            self.basic_attack()

        self.handle_walk_sound()

    def input(self, key):
        super().input(key)
        print("PLAYER INPUT:", key)
        if key == 'escape' and in_game:
            pause_game()
        if key == 'q' and in_game:
            player.cursor.visible = False
            toggle_inventory()    

    def handle_walk_sound(self):
            
        moving = (
            held_keys['w'] or
            held_keys['a'] or
            held_keys['s'] or
            held_keys['d']
        )

        if moving and self.grounded:

            if not self.walk_sound.playing:
                self.walk_sound.play()

        else:

            if self.walk_sound.playing:
                self.walk_sound.stop()

    def basic_attack(self):

        if self.attack_cooldown <= 0:
            print('Necromancer Attack')
            self.attack_cooldown = 0.5


def load_level_data(level_number):
    file_path = f'database/levels/level_{level_number}.csv'

    if not os.path.exists(file_path):
        print('Level database not found')
        return []

    level_data = []

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            level_data.append(row)

    return level_data


def clear_menu():
    global menu_entities

    menu_music.stop()

    for e in menu_entities:
        destroy(e)

    menu_entities = []


def continue_game():
    player.cursor.visible = True
    global game_paused

    mouse.locked = True
    game_paused = False

    for e in pause_menu_entities:
        destroy(e)

    pause_menu_entities.clear()


def return_to_main_menu():
    global game_paused
    global room_entities
    global player
    global in_game
    in_game = False

    mouse.locked = False
    game_paused = False

    for e in pause_menu_entities:
        destroy(e)

    pause_menu_entities.clear()

    for e in room_entities:
        destroy(e)

    room_entities.clear()

    if player:
        destroy(player)

    main_menu()


def pause_game():
    player.cursor.visible = False
    global game_paused

    if game_paused:
        return

    game_paused = True
    mouse.locked = False

    pause_title = Text(
        text='GAME PAUSED',
        origin=(0, 0),
        scale=2,
        y=0.2
    )

    continue_button = Button(
        text='Continue',
        texture='resources/images/buttons.png',
        color=color.rgba(255, 255, 255, 0),
        scale=(0.3, 0.1),
        y=0
    )

    continue_button_background = Entity(
                parent=camera.ui,
                model='quad',
                texture='resources/images/buttons.png',
                scale=(0.3, 0.1),
                )

    quitpause_button = Button(
        text='Quit Game',
        texture='resources/images/buttons.png',
        scale=(0.3, 0.1),
        color=color.rgba(255, 255, 255, 0),
        y=-0.3
    )

    quitpause_button_background = Entity(
                    parent=camera.ui,
                    model='quad',
                    texture='resources/images/buttons.png',
                    scale=(0.3, 0.1),
                    y=-0.3
                    )

    main_menu_button = Button(
        text='Main Menu',
        scale=(0.3, 0.1),
        color=color.rgba(255, 255, 255, 0),
        y=-0.15
    )

    main_menu_button_background = Entity(
                        parent=camera.ui,
                        model='quad',
                        texture='resources/images/buttons.png',
                        scale=(0.3, 0.1),
                        y=-0.15
                        )

    continue_button.on_click = continue_game
    quitpause_button.on_click = quit_game
    main_menu_button.on_click = return_to_main_menu

    pause_menu_entities.extend([
        pause_title,
        continue_button,
        quitpause_button,
        main_menu_button,
        continue_button_background,
        quitpause_button_background,
        main_menu_button_background
    ])


def spawn_level_creatures(level_data):
    spawn_x = -10

    for creature in level_data:
        Entity(
            model='cube',
            color=color.red,
            scale=(1.5, 2, 1.5),
            position=(spawn_x, 1, 8),
            collider='box'
        )

        Text(
            text=creature['name'],
            position=(-0.85, 0.45 - (spawn_x * 0.002)),
            scale=1
        )

        spawn_x += 4


def start_game():
    global player
    global room_entities
    global in_game
    in_game = True

    clear_menu()
    menu_music.stop()

    player, room_entities = build_level(
        necromancer,
        GamePlayer
    )

    level_data = load_level_data(current_level)

    print('Loaded Level Data:', level_data)

    spawn_level_creatures(level_data)


def quit_game():
    application.quit()

"""
def input(key):
    print(f"Key pressed: {key}")
    if key == 'escape':
        pause_game()
    if key == 'q' and in_game:
        player.cursor.visible = False
        toggle_inventory()
"""

def open_settings_menu():

    clear_menu()

    open_settings(main_menu)


def main_menu():

    menu_music.play()

    menu_bg = Entity(
        parent=camera.ui,
        model='quad',
        texture='resources/images/background_menu.png',
        scale=(2, 1),
        z=1
    )

    title = Text(
        text='Le trône du nécromancien',
        parent=camera.ui,
        origin=(0, 0),
        scale=3,
        y=0.3
    )

    subtitle = Text(
        text='Necromancer Level up',
        parent=camera.ui,
        origin=(0, 0),
        scale=1.2,
        y=0.2
    )

    start_button = Button(
    parent=camera.ui,
    texture='resources/images/buttons.png',
    text='Start Game',
    scale=(0.25, 0.1),
    color=color.rgba(255, 255, 255, 0),
    position=(0, -0.39)
    )

    start_button_background = Entity(
    parent=camera.ui,
    model='quad',
    texture='resources/images/buttons.png',
    scale=(0.25, 0.1),
    position=(0, -0.39),
    )

    settings_button = Button(
    parent=camera.ui,
    texture='resources/images/buttons.png',
    text='Settings',
    scale=(0.25, 0.1),
    color=color.rgba(255, 255, 255, 0),
    position=(-0.35, -0.29)
    )

    settings_button_background = Entity(
        parent=camera.ui,
        model='quad',
        texture='resources/images/buttons.png',
        scale=(0.25, 0.1),
        position=(-0.35, -0.29)
        )

    quit_button = Button(
        parent=camera.ui,
        texture='resources/images/buttons.png',
        text='Quit Game',
        scale=(0.25, 0.1),
        color=color.rgba(255, 255, 255, 0),
        position=(0.35, -0.29)
    )

    quit_button_background = Entity(
            parent=camera.ui,
            model='quad',
            texture='resources/images/buttons.png',
            scale=(0.25, 0.1),
            position=(0.35, -0.29)
            )

    playerIMG = Entity(
    parent=camera.ui,
    model='quad',
    texture='resources/images/player.png',
    scale=(0.5, 0.5),
    position=(0.26, -0.08),
    origin=(0.5, 0),
    z=0
    )

    settings_button.on_click = open_settings_menu

    start_button.on_click = lambda: (
    clear_menu(),
    start_intro(start_game)
    )
    quit_button.on_click = quit_game

    menu_entities.extend([
        menu_bg,
        title,
        subtitle,
        start_button,
        quit_button,
        playerIMG,
        settings_button,
        start_button_background,
        quit_button_background,
        settings_button_background
    ])


main_menu()
app.run()