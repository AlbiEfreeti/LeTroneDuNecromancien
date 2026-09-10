from ursina import *

intro_entities = []

with open('resources/texts/intro_text.txt', 'r', encoding='utf-8') as file:
    intro_story = file.read()


def start_intro(start_level_function):

    background = Entity(
        parent=camera.ui,
        model='quad',
        texture='resources/images/background_intro.png',
        scale=(2, 1),
        z=0
    )

    text = Text(
        parent=camera.ui,
        text=intro_story,
        text_color=color.white,
        origin=(0, 0),
        scale=1.5,
        y=0,
        z=-1
    )

    skip_button = Button(
        parent=camera.ui,
        text='Skip',
        scale=(0.2, 0.08),
        y=-0.4,
        text_color=color.white,
        color=color.rgba(0,0,0,0),
        highlight_color=color.rgba(0,0,0,0),
        pressed_color=color.rgba(0,0,0,0),
        z=-1
    )

    music = Audio(
        'resources/audio/Black_Velvet_Relic.mp3',
        autoplay=True,
        loop=True
    )

    intro_entities.extend([
        background,
        text,
        skip_button
    ])

    def skip():

        music.stop()

        for e in intro_entities:
            destroy(e)

        intro_entities.clear()

        start_level_function()

    skip_button.on_click = skip