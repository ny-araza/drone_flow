from typing import Any

import pygame as pg

from src.drones import Drone
from src.zone import Zone

from .color import color_rgb
from .parse import Parse
from .utils import Utils


class Display:
    def __init__(
        self,
        map_path: str,
        width: int = 1280,
        height: int = 960,
        size_pixel: int = 50,
        cell_size: int = 60,
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
        self.font = pg.font.Font(None, 24)

    def display_window(self) -> None:
        running = True
        dragging = False

        boxes = []
        color = []

        offset_x = 0
        offset_y = 0

        start_box_x = 0
        start_box_y = 0

        for zone in self.parse.list_zones:
            new_x, new_y = zone.x * self.cell_size, zone.y * self.cell_size

            rect_initial_pos = pg.Rect(
                new_x, new_y, self.cell_size // 2, self.cell_size // 2
            )

            center_x = new_x + self.cell_size // 2
            center_y = new_y + self.cell_size // 2

            if zone.is_start:
                start_box_x = center_x
                start_box_y = center_y

            rect_initial_pos.center = (center_x, center_y)

            boxes.append(rect_initial_pos)
            color.append(zone.color)

        list_drones: list[Drone] = []

        for i in range(self.parse.nb_drones):
            new_drone = Drone(start_box_x, start_box_y, "./images/drone_50x50.png")

            list_drones.append(new_drone)

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.KEYDOWN:
                    if event.key == 1073741910:
                        if self.cell_size <= 30:
                            break
                        self.cell_size -= 5
                        for i, zone in enumerate(self.parse.list_zones):
                            boxes[i].w = self.cell_size // 2
                            boxes[i].h = self.cell_size // 2

                            boxes[i].x = zone.x * self.cell_size + offset_x

                            boxes[i].y = zone.y * self.cell_size + offset_y

                    if event.key == 1073741911:
                        if self.cell_size >= 200:
                            break
                        self.cell_size += 5
                        for i, zone in enumerate(self.parse.list_zones):
                            boxes[i].w = self.cell_size // 2
                            boxes[i].h = self.cell_size // 2

                            boxes[i].x = zone.x * self.cell_size + offset_x

                            boxes[i].y = zone.y * self.cell_size + offset_y

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        dragging = True

                    elif event.button == 4:
                        if self.cell_size >= 200:
                            break
                        self.cell_size += 5
                        for i, zone in enumerate(self.parse.list_zones):
                            boxes[i].w = self.cell_size // 2
                            boxes[i].h = self.cell_size // 2

                            boxes[i].x = zone.x * self.cell_size + offset_x

                            boxes[i].y = zone.y * self.cell_size + offset_y

                    elif event.button == 5:
                        if self.cell_size <= 30:
                            break
                        self.cell_size -= 5
                        self.font.size("24")
                        for i, zone in enumerate(self.parse.list_zones):
                            boxes[i].w = self.cell_size // 2
                            boxes[i].h = self.cell_size // 2

                            boxes[i].x = zone.x * self.cell_size + offset_x

                            boxes[i].y = zone.y * self.cell_size + offset_y

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

                text = self.font.render(
                    self.parse.list_zones[i].name, True, color_rgb["WHITE"]
                )

                text_rect = text.get_rect()
                text_rect.midtop = (box.centerx, box.bottom + 5)

                self.screen.blit(text, text_rect)        

            for conn in self.parse.list_connections:
                zone1_pos = (0, 0)
                zone2_pos = (0, 0)

                for zone in self.parse.list_zones:
                    if conn.zone1.name == zone.name:
                        index = self.parse.list_zones.index(zone)
                        zone1_pos = boxes[index].center

                    if conn.zone2.name == zone.name:
                        index = self.parse.list_zones.index(zone)
                        zone2_pos = boxes[index].center

                pg.draw.line(self.screen, color_rgb["WHITE"], zone1_pos, zone2_pos, 2)

                if conn.zone1.is_start:
                    pg.draw.circle(self.screen, color_rgb["MAROON"], zone1_pos, 10)
                

            #######################################################

            #######################################################

            pg.display.flip()
