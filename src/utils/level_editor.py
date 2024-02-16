""" Blocks for in-game level editor """

from sprites.apple import Apple
from sprites.backdrop import Backdrop
from sprites.blood import Blood
from sprites.burger import Burger
from sprites.capybara import Capybara
from sprites.chainsaw import Chainsaw
from sprites.chicken import Chicken
from sprites.coin import Coin
from sprites.cow import Cow
from sprites.destroyable import Destroyable
from sprites.dog import Dog
from sprites.duck import Duck
from sprites.fence import Fence
from sprites.fly import Fly
from sprites.frog import Frog
from sprites.fuel import Fuel
from sprites.hammer import Hammer
from sprites.kitten import Kitten
from sprites.landmine import LandMine
from sprites.lava import Lava
from sprites.levelexit import LevelExit
from sprites.piggybank import PiggyBank
from sprites.sheep import Sheep
from sprites.skeleton import Skeleton
from sprites.sword import Sword
from sprites.tv import TV
from sprites.wall import Wall
from sprites.water import Water
from sprites.wood import Wood
from utils.image import ImageCache


def get_editor_blocks(sprites_dir: str, image_cache: ImageCache) -> list:
    """ Returns the items for the in-game block editor """
    return [
        Backdrop(
            sprites_dir,
            image_cache,
            'placeholder.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gras1.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gras2.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gras3.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'cornfield.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'mud.jpg'
        ),
        Destroyable(
            sprites_dir,
            image_cache,
            'tree1.png'
        ),
        Destroyable(
            sprites_dir,
            image_cache,
            'tree2.png'
        ),
        Destroyable(
            sprites_dir,
            image_cache,
            'tree3.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'cactus1.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'tropical.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'pebble.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'highway1.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'snow.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'grid1.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'grid2.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'shoes.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'basket.png'
        ),
        Destroyable(
            sprites_dir,
            image_cache,
            'box.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'wrench1.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'wrench2.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'wrench3.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'wrench4.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'stool.png'
        ),
        Destroyable(
            sprites_dir,
            image_cache,
            'tree3.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'rhodes1.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'rhodes2.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'sand.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gravel.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower1.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower2.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower3.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower4.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower5.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'nymphaea1.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'nymphaea2.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'nymphaea3.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'nymphaea4.png'
        ),
        Wall(
            sprites_dir,
            image_cache
        ),
        Water(
            sprites_dir,
            image_cache
        ),
        Lava(
            sprites_dir,
            image_cache
        ),
        Wood(
            sprites_dir,
            image_cache
        ),
        Fence(
            sprites_dir,
            image_cache,
            'wood_fence_horizontal.png'
        ),
        Fence(
            sprites_dir,
            image_cache,
            'wood_fence_vertical.png'
        ),
        Chainsaw(
            sprites_dir,
            image_cache
        ),
        Sword(
            sprites_dir, image_cache
        ),
        Fuel(
            sprites_dir,
            image_cache
        ),
        Hammer(
            sprites_dir,
            image_cache
        ),
        Coin(
            sprites_dir,
            image_cache
        ),
        PiggyBank(
            sprites_dir,
            image_cache
        ),
        Apple(
            sprites_dir,
            image_cache
        ),
        Burger(
            sprites_dir,
            image_cache
        ),
        Blood(
            sprites_dir,
            image_cache
        ),
        Chicken(
            sprites_dir,
            image_cache
        ),
        Kitten(
            sprites_dir,
            image_cache
        ),
        Skeleton(
            sprites_dir,
            image_cache
        ),
        Sheep(
            sprites_dir,
            image_cache
        ),
        Cow(
            sprites_dir,
            image_cache
        ),
        Dog(
            sprites_dir,
            image_cache
        ),
        Duck(
            sprites_dir,
            image_cache
        ),
        Frog(
            sprites_dir,
            image_cache
        ),
        Capybara(
            sprites_dir,
            image_cache
        ),
        LevelExit(
            sprites_dir,
            image_cache
        ),
        LandMine(
            sprites_dir,
            image_cache
        ),
        TV(
            sprites_dir,
            image_cache
        ),
        Fly(
            sprites_dir,
            image_cache
        )
    ]
