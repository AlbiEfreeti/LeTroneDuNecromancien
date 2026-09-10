from ursina import *

settings_entities = []


def open_settings(close_callback):

    mouse.locked = False

    settings_bg = Entity(
        parent=camera.ui,
        model='quad',
        texture='resources/images/settings_player.png',
        scale=(2, 1),
        z=1
    )

    settings_entities.append(settings_bg)

    return_button = Button(
        parent=camera.ui,
        text='Return to Menu',
        scale=(0.25, 0.1),
        color=color.black,
        position=(0.35, -0.29)
    )

    settings_entities.append(return_button)
    return_button.on_click = lambda: close_settings(close_callback)

    settings_bg.input = input


def close_settings(close_callback):

    for e in settings_entities:
        destroy(e)

    settings_entities.clear()

    close_callback()
