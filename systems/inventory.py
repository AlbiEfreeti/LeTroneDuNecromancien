from ursina import *
from systems.database_loader import load_spells

inventory_open = False
inventory_ui = []
spell_text = None

default_spell_scale = (0.115, 0.125) #DEFAULT FOR INVENTORY PNG INVENTORY 2

# Load spell database
spells = load_spells()

def toggle_inventory():
    global inventory_open

    if inventory_open:
        close_inventory()
    else:
        open_inventory()


def open_inventory():
    global inventory_open
    global inventory_ui
    global spell_text

    mouse.locked = False
    inventory_open = True

    background = Entity(
        parent=camera.ui,
        model='quad',
        texture='resources/inventory/inventory_2.png',
        scale=(1.3, 0.8),
        z=0
    )

    inventory_ui.append(background)

    #ITEM OR SPELL TEXT RIGHT POSITION AND SCALE 
    spell_text = Text(
        text='SPELL/ITEM TEXT: Description and details of the selected spell or item will appear here.',
        parent=camera.ui,
        origin=(0,0),
        position=(0,-0.075),
        scale=0.9,
        color=color.white,
        z=-1
    )

    inventory_ui.append(spell_text)

    ####################################################################
    ########## SPELL ICONS IN INVENTORY ##########
    ####################################################################

    spell1 = spells[6] #access spell database
    spell2 = spells[1] #access spell database

    spell_11 = Entity(
        parent=camera.ui,
        model='quad',
        texture=f"resources/spell_icons/spell{spell1['id']}.png",
        position=(-0.479, -0.197),      # Spell slot position 1 left
        scale=default_spell_scale,
        z=-0.1
    )

    spell_12 = Entity(
        parent=camera.ui,
        model='quad',
        texture=f"resources/spell_icons/spell{spell2['id']}.png",
        position=(-0.365, -0.197),      # Spell slot position 2 left
        scale=default_spell_scale, 
        z=-0.1
    )

    inventory_ui.append(spell_12)
    inventory_ui.append(spell_11)

    item_11 = Entity(
        parent=camera.ui,
        model='quad',
        texture=f"resources/item_icons/spell{spell2['id']}.png",
        position=(-0.365, -0.197),      # Spell slot position 2 left
        scale=default_spell_scale, 
        z=-0.1
    )

    #####################################################################
    ########### END OF SPELL ICONS IN INVENTORY ##########
    #####################################################################

def close_inventory():
    global inventory_open
    global inventory_ui
    global spell_text

    mouse.locked = True
    inventory_open = False

    for e in inventory_ui:
        destroy(e)

    inventory_ui.clear()

    spell_text = None

