import arcade

MARGIN = 10
DEBUG_COLOR = arcade.csscolor.GHOST_WHITE

DEFAULT_FONT = 'Laila'
ADRIP_FONT = 'a dripping marker'
MONOTYPE_FONT = 'Consolas Mono Book'

EXTRA_SMALL_FONT_SIZE = 10
SMALL_FONT_SIZE = 12  #
MEDIUM_FONT_SIZE = 14
LOGO_FONT_SIZE = 80

DEBUG_FONT_SIZE = SMALL_FONT_SIZE


def create_text(
        text,
        start_x=MARGIN,
        start_y=MARGIN,
        color=arcade.csscolor.WHITE,
        font_size=MEDIUM_FONT_SIZE,
        font_name=DEFAULT_FONT,
        anchor_x='left',
        anchor_y='bottom',
        align='left',
        width=None,
        multiline=False
):
    return arcade.Text(
        text=text,
        start_x=start_x,
        start_y=start_y,
        color=color,
        font_size=font_size,
        align=align,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        width=width,
        multiline=multiline,
        font_name=font_name
    )


def get_style():
    return {
        'font_name': DEFAULT_FONT
    }

def label_value(label: str, value: any) -> str:
    """
    @param label: label text
    @param value: value
    @return:
    """
    return ': '.join([label, str(value)])


def draw_debug(player_sprite, window):
    debug_lines = []

    if not window.show_fps:
        return

    if player_sprite:
        debug_lines.append(
            label_value('POS', str(int(player_sprite.center_x)) + ' ' + str(int(player_sprite.center_y)))
        )

    debug_lines.append(label_value('FPS', str(int(arcade.get_fps()))))

    create_text(
        "\n".join(debug_lines),
        width=window.width - (MARGIN * 2),
        align='right',
        color=DEBUG_COLOR,
        font_name=MONOTYPE_FONT,
        font_size=DEBUG_FONT_SIZE,
        multiline=True
    ).draw()
