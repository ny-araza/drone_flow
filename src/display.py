from .utils import Utils
from .parse import Parse
import pygame as pg
from .color import color_rgb
from typing import Any


class Display:
    def __init__(
            self, map_path: str,
            width: int = 1280,
            height: int = 960,
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

        self.list_rect = []
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()

    def display_window(self) -> None:
        running = True

        boxes = []

        for zone in self.parse.list_zones:
            new_x, new_y = zone.x * self.cell_size, zone.y * self.cell_size
            temp = pg.Rect(new_x, new_y, self.cell_size, self.cell_size)
            boxes.append(temp)

        print(boxes)

        active_box = None
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for num, box in enumerate(boxes):
                            if box.collidepoint(event.pos):
                                active_box = num

                if event.type == pg.MOUSEMOTION:
                    if active_box != None:
                        for box in boxes:
                            box.move_ip(event.rel)
                
                if event.type == pg.MOUSEBUTTONUP:
                    active_box = None

            self.screen.fill((0, 0, 0))

            for box in boxes:
                pg.draw.rect(self.screen, color_rgb["PURPLE"], box)


            pg.display.flip()
    