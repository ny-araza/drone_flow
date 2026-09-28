from .utils import Utils
from .parse import Parse
import pygame as pg
from .connection import Connection

class Display:
    def __init__(
            self, map_path: str,
            width: int = 1280,
            height: int = 720,
            size_pixel: int = 50,
            ):
        self.parse: Parse = Parse()
        temp_data = Utils.read_file(map_path)
        self.parse.parse(temp_data)
        self.width = width
        self.height = height
        self.size_pixel = size_pixel

        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()


    def display_window(self) -> None:
        runing = True
        while runing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    runing = False
            self.display_connection()
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()

    def display_images(
        self, pos_x: int, 
        pos_y: int, path: str,
        is_start: bool = False
    ) -> None:
        if not is_start:
            if pos_x < 0:
                rx = pos_x - self.size_pixel
            else:
                rx = pos_x + self.size_pixel
            if pos_y < 0:
                ry = pos_y - self.size_pixel
            else:
                ry = pos_y + self.size_pixel
        else:
            rx = pos_x
            ry = pos_y
        image_loaded = pg.image.load(path).convert_alpha()
        self.screen.blit(
            image_loaded, (
                rx,
                ry
            )
        )

    def display_connection(self) -> None:
        # self.screen.fill("purple")
        for index, zone in enumerate(self.parse.list_zones):
            if zone.is_start or zone.is_end:
                self.display_images(zone.x, zone.y, zone.image, zone.is_start)
