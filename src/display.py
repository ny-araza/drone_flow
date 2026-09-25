from .utils import Utils
from .parse import Parse
import pygame as pg

class Display:
    def __init__(
            self, map_path: str, 
            width: int = 1280, 
            height: int = 720
            ):
        parse: Parse = Parse()
        temp_data = Utils.read_file(map_path)
        parse.parse(temp_data)
        self.data: Parse = parse
        self.width = width
        self.height = height

    def display_window(self) -> None:
        pg.init()
        screen = pg.display.set_mode((self.width, self.height))
        clock = pg.time.Clock()
        runing = True
        while runing:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == 768:
                    runing = False
            screen.fill("purple")
            pg.display.flip()
            clock.tick(60)
        pg.quit()