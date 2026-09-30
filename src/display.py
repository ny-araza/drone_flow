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
        dragging = False

        boxes = []
        color = []

        offset_x = 0
        offset_y = 0

        for zone in self.parse.list_zones:
            new_x, new_y = zone.x * self.cell_size, zone.y * self.cell_size
            temp = pg.Rect(new_x, new_y, self.cell_size, self.cell_size)
            boxes.append(temp)
            color.append(zone.color)

        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        dragging = True

                    elif event.button == 4:
                        self.cell_size += 5
                        for i, zone in enumerate(self.parse.list_zones):
                            boxes[i].w = self.cell_size
                            boxes[i].h = self.cell_size

                            boxes[i].x = (
                                zone.x * self.cell_size + offset_x
                            )

                            boxes[i].y = (
                                zone.y * self.cell_size + offset_y
                            )

                    elif event.button == 5:
                        self.cell_size -= 5
                        for i, zone in enumerate(self.parse.list_zones):
                            boxes[i].w = self.cell_size
                            boxes[i].h = self.cell_size

                            boxes[i].x = (
                                zone.x * self.cell_size + offset_x
                            )
                            
                            boxes[i].y = (
                                zone.y * self.cell_size + offset_y
                            )

                elif event.type == pg.MOUSEMOTION:
                    if dragging:
                        for box in boxes:
                            dx, dy = event.rel
                            box.move_ip((dx, dy))

                        offset_x += dx
                        offset_y += dy

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False

            self.screen.fill((0, 0, 0))

            for i, box in enumerate(boxes):
                pg.draw.rect(self.screen, color_rgb[color[i].upper()], box)

            pg.display.flip()
