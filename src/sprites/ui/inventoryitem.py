import os
import uuid

import PIL
import arcade
from PIL import ImageDraw, ImageFont
from arcade import get_four_byte_color

PADDING = 10
TEXT_PADDING = (28, 5)
ALPHA = 80

# Add transparency to colors
r, g, b, a = arcade.csscolor.BLACK
a = ALPHA
COLOR_DEFAULT = r, g, b, a

# Add transparency to colors
r, g, b, a = arcade.csscolor.DARK_GREY
a = ALPHA
COLOR_SELECTED = r, g, b, a


class InventoryItem(arcade.sprite.Sprite):

    def __init__(self, filename, bottom, left):
        super().__init__(filename=filename)
        self.bottom = bottom
        self.left = left
        self.image = PIL.Image.open(filename).convert('RGBA').crop()
        self.selected = False
        self.names = None
        self.item = None
        self.state = None
        self.quantity = 0

    def setup(self, state, selected=False, item=None):
        self.state = state
        self.selected = selected
        self.set_item(item)

    def get_item(self):
        return self.item

    def set_item(self, item):
        self.item = item
        self.generate_cache_names()
        self.quantity = 1
        self.update_sprite(self.selected)

    def generate_cache_names(self):
        self.names = [
            uuid.uuid4().hex,
            uuid.uuid4().hex
        ]

    def select(self):
        self.update_sprite(True)

    def unselect(self):
        self.update_sprite(False)

    def update_sprite(self, selected=False):
        self.selected = selected

        color = COLOR_DEFAULT

        if self.selected:
            color = COLOR_SELECTED

        name = self.names[int(self.selected)]
        image = PIL.Image.new("RGBA", self.image.size, get_four_byte_color(color))

        image.paste(self.image, (0, 0), self.image)

        width = self.width - PADDING
        height = self.height - PADDING * 2

        x = 0
        y = 0

        if self.item:
            scaled_item = PIL.ImageOps.pad(self.item.image, (int(width), int(height)))
            x, y = int(self.width / 2), int(self.height / 2)

            x -= int(scaled_item.width / 2)
            y -= int(scaled_item.height / 2)

            image.paste(scaled_item, (x, y), scaled_item)

        fontfile = os.path.join(self.state.font_dir, 'consolamonobook.ttf')
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(fontfile, 14)
        text = str(self.quantity).rjust(3, ' ')

        # If there is no item don't show the count
        if not self.item:
            text = ''

        # drawing text size
        draw.text(
            TEXT_PADDING,
            str(text),
            font=font,
            fill=arcade.csscolor.WHITE
        )

        texture = arcade.texture.Texture(name=name, image=image)

        self.texture = texture

    def push(self):
        self.generate_cache_names()

        self.quantity += 1
        self.update_sprite(self.selected)

    def pop(self):
        self.generate_cache_names()

        self.quantity -= 1

        if self.quantity <= 0:
            self.quantity = 0
            self.item = None

        self.update_sprite(self.selected)

        return self.quantity

    def __str__(self):
        if not self.item:
            return 'No Item'
        return self.item.__class__.__name__ + ' ' + str(self.quantity)
