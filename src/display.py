from .utils import Utils
from .parse import Parse
import pygame as pg

class Display:
    def __init__(self, map_path: str):
        parse: Parse = Parse()
        data = Utils.read_file(map_path)
        parse.parse(data)


def tes_display() -> None:
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            # get the quit event
            if event.type == pg.QUIT:
                return
        screen.fill("purple")
        pg.display.flip()
        clock.tick(60)
    pg.quit()