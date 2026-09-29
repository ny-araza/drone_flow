from .utils import Utils
from .parse import Parse
import pygame as pg
from .color import color_rgb
from typing import Any

class Display:
    def __init__(
            self, map_path: str,
            width: int = 1500,
            height: int = 900,
            size_pixel: int = 50,
            cell_size: int = 60
            ):
        self.parse: Parse = Parse()
        temp_data = Utils.read_file(map_path)
        self.parse.parse(temp_data)
        self.width = width
        self.height = height
        self.size_pixel = size_pixel
        self.cell_size = cell_size

        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

    def display_window(self) -> None:
        runing = True
        while runing:
            for event in pg.event.get():
                if event.type == pg.MOUSEMOTION:
                    print(pg.mouse.get_pos())
                if event.type == pg.QUIT:
                    runing = False
            self.display_zone()
            pg.display.flip()
            self.clock.tick(60)
        pg.quit()

    def display_images(
        self, pos_x: int, 
        pos_y: int, path: str,
        is_start: bool = False
    ) -> None:
        rx = pos_x
        ry = pos_y
        image_loaded = pg.image.load(path).convert_alpha()
        self.screen.blit(image_loaded, (rx, ry))

    def display_connection(self) -> None:
        self.screen.fill("purple")
        for index, zone in enumerate(self.parse.list_zones):
            if zone.is_start or zone.is_end:
                self.display_images(zone.x, zone.y, zone.image, zone.is_start)

    def draw_circle(
            self, pos_x: int, 
            pos_y: int, color: tuple[int, int, int],
            width: int
            ) -> None:
        pg.draw.circle(
            self.screen, 
            color,
            (pos_x, pos_y),
            width
            )

    def draw_rect(
            self,
            color: tuple[int, int, int],
            pos_x, pos_y,
            width: int,
            height: int
    ) -> None:
        pg.draw.rect(
            self.screen,
            color,
            pg.Rect(pos_x, pos_y, width, height)
        )

    def display_zone(self) -> None:
        for zone in self.parse.list_zones:
            new_x = zone.x * self.cell_size
            new_y = zone.y * self.cell_size
            
            rect_initial_pos = pg.Rect(
                new_x, new_y,
                self.cell_size // 2, self.cell_size // 2
            )

            center_x = new_x + self.cell_size // 2
            center_y = new_y + self.cell_size // 2

            rect_initial_pos.center = (center_x, center_y)
            pg.draw.rect(
                self.screen, color_rgb[zone.color.upper()], 
                rect_initial_pos, 0
            )
