import threading

import pygame as pg
from pygame.image import load

from src.drones import Drone
from src.planner import Action, Planner
from src.zone import Zone

from .color import color_rgb
from .parse import Parse
from .utils import Utils

MIN_CELL = 50
MAX_CELL = 200
ZOOM_STEP = 5
FPS = 60
MAX_ZONE_FONT = 24
MIN_ZONE_FONT = 10


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
        self.cell_size = cell_size
        self.list_rect = []
        self.boxes: list[pg.Rect] = []
        self.offset_x = 0
        self.offset_y = 0
        pg.init()
        self.screen = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 24)

    def _update_boxes(self) -> None:
        half = self.cell_size // 2
        for box, zone in zip(self.boxes, self.parse.list_zones):
            box.size = (half, half)
            box.center = (
                zone.x * self.cell_size + half + self.offset_x,
                zone.y * self.cell_size + half + self.offset_y,
            )

    def _zoom(self, step: int) -> None:
        new_size = self.cell_size + step
        if not MIN_CELL <= new_size <= MAX_CELL:
            return
        self.cell_size = new_size
        self._update_boxes()

    def draw_loading(self, angle: int) -> None:
        center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

        radius = 40

        # Cercle extérieur
        pg.draw.circle(self.screen, (80, 80, 80), center, radius, 5)

        # Point qui tourne
        import math

        rad = math.radians(angle)

        x = center[0] + int(math.cos(rad) * radius)
        y = center[1] + int(math.sin(rad) * radius)

        pg.draw.circle(self.screen, (0, 200, 255), (x, y), 8)

        # Texte
        font = pg.font.Font(None, 36)

        text = font.render("Calcul du plan...", True, (255, 255, 255))

        text_rect = text.get_rect(center=(center[0], center[1] + 80))

        self.screen.blit(text, text_rect)

    def display_window(self) -> None:
        running = True
        dragging = False

        zones = self.parse.list_zones
        zone_index = {zone.name: i for i, zone in enumerate(zones)}

        start_zone: Zone = Zone(
            name="start",
            x=0,
            y=0,
            color=color_rgb["WHITE"],
        )
        colors = []

        for zone in zones:
            self.boxes.append(pg.Rect(0, 0, 0, 0))
            colors.append(zone.color)
            if zone.is_start:
                start_zone = zone

        self._update_boxes()

        plans: list[list[Action]] = []
        loading = True

        def start_planning():
            nonlocal plans, loading
            plans = []
            loading = True

            def calculate():
                nonlocal plans, loading
                local_planner = Planner(
                    zones,
                    self.parse.list_connections,
                    self.parse.nb_drones,
                )
                result = local_planner.plan_all()
                plans = result
                loading = False

            threading.Thread(target=calculate, daemon=True).start()

        start_planning()

        list_drones: list[Drone] = [
            Drone(start_zone.x, start_zone.y, "./images/drone_50x50.png")
            for _ in range(self.parse.nb_drones)
        ]

        total_turns = 0
        current_turn = 0
        finished = False
        dt = 0.0
        restart = False
        pause = False
        angle = 0

        restart_option_label = "<R> to restart"

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_KP_MINUS, pg.K_MINUS):
                        self._zoom(-ZOOM_STEP)
                    elif event.key in (pg.K_KP_PLUS, pg.K_PLUS):
                        self._zoom(ZOOM_STEP)

                    elif event.key == pg.K_r:
                        restart = True

                    elif event.key == pg.K_SPACE:
                        pause = not pause

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        dragging = True
                    elif event.button == 4:
                        self._zoom(ZOOM_STEP)
                    elif event.button == 5:
                        self._zoom(-ZOOM_STEP)

                elif event.type == pg.MOUSEMOTION and dragging:
                    dx, dy = event.rel
                    self.offset_x += dx
                    self.offset_y += dy
                    self._update_boxes()

                elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                    dragging = False

            self.screen.fill((0, 0, 0))

            if loading:
                print(loading)
                self.draw_loading(angle)

                angle = (angle + 5) % 360

                pg.display.flip()
                dt = self.clock.tick(FPS) / 1000

                continue

            total_turns = max(
                (len(p) for p in plans),
                default=0,
            )

            if finished and restart:
                list_drones = [
                    Drone(start_zone.x, start_zone.y, "./images/drone_50x50.png")
                    for _ in range(self.parse.nb_drones)
                ]
                finished = False
                current_turn = 0
                dt = 0.0

                start_planning()

            for conn in self.parse.list_connections:
                pos1 = self.boxes[zone_index[conn.zone1.name]].center
                pos2 = self.boxes[zone_index[conn.zone2.name]].center
                pg.draw.line(self.screen, color_rgb["WHITE"], pos1, pos2, 2)

            show_names = self.cell_size > MIN_CELL
            zone_font = pg.font.Font(None, 24) if show_names else None
            margin = max(2, self.cell_size // 12)

            for i, box in enumerate(self.boxes):
                pg.draw.rect(self.screen, color_rgb[colors[i].upper()], box)

                if zone_font is not None:
                    text = zone_font.render(zones[i].name, True, color_rgb["WHITE"])
                    text_rect = text.get_rect()
                    text_rect.midtop = (box.centerx, box.bottom + margin)
                    self.screen.blit(text, text_rect)

            if not finished and not any(d.moving for d in list_drones):
                current_turn += 1
                if current_turn > total_turns:
                    finished = True
                    restart = False
                    current_turn -= 1
                else:
                    for drone, plan in zip(list_drones, plans):
                        if current_turn <= len(plan):
                            action = plan[current_turn - 1]
                            if action is not None:
                                drone.target = action
                                drone.moving = True

            for i, drone in enumerate(list_drones):
                if drone.moving and drone.target is not None:
                    if drone.move_to(drone.target[0], drone.target[1], dt):
                        drone.turn += 1
                        drone.moving = False

                drone.draw(self.screen, self.cell_size, self.offset_x, self.offset_y)

                sx, sy = drone.screen_pos(self.cell_size, self.offset_x, self.offset_y)
                label = self.font.render(
                    f"D{i + 1}: {drone.turn}", True, color_rgb["WHITE"]
                )
                label_rect = label.get_rect()
                label_rect.midbottom = (sx, sy - self.cell_size // 4)
                self.screen.blit(label, label_rect)
            turn_text = self.font.render(
                f"Tour : {current_turn}" + (" (terminé)" if finished else ""),
                True,
                color_rgb["WHITE"],
            )
            self.screen.blit(turn_text, (10, 10))

            turn_text = self.font.render(
                restart_option_label,
                True,
                color_rgb["WHITE"],
            )
            self.screen.blit(
                turn_text, (self.width - (100 + len(restart_option_label)), 10)
            )

            pg.display.flip()
            dt = self.clock.tick(FPS) / 1000
        pg.quit()
