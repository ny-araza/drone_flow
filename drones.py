import pygame as pg


class Drone:
    """Represent the drone

        Attributes:
            x (float): the x exact position in pygame screen
            y (float): the y exact position in pygame screen
            image (str): The path of the drone image
    """
    def __init__(self, x: float, y: float, image: str) -> None:

        self.x = x
        self.y = y

        self.turn = 0

        self.image = pg.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

        self.speed = 3.0

        self.target: tuple[float, float] | None = None
        self.moving = False

        self._scaled_image: pg.Surface | None = None
        self._scaled_size = 0

    def move_to(self, target_x: float, target_y: float, dt: float) -> bool:
        """Caclulate if the drone is arrived to the dest or not

            Args:
                target_x (float): x position of target in pygame screen
                target_y (float): y position of target in pygame screen
                dt (float): time elapsed

            Returns:
                bool
        """
        dx = target_x - self.x
        dy = target_y - self.y

        distance = (dx**2 + dy**2) ** 0.5
        step = self.speed * dt

        if distance <= step:
            self.x = target_x
            self.y = target_y
            return True

        self.x += dx / distance * step
        self.y += dy / distance * step

        return False

    def screen_pos(
        self, cell_size: int, offset_x: int, offset_y: int
    ) -> tuple[int, int]:
        """Convert the pos in map to a exact screen pos

            Args:
                cell_size (int): The size of the box's zone
                offset_x (int): Use if the user move the entire map
                    . Its a represent the mouse x pos
                offset_x (int): its represents the y pos mouse.

            Returns:
                tuple[int, int]
        """
        return (
            int(self.x * cell_size + cell_size // 2 + offset_x),
            int(self.y * cell_size + cell_size // 2 + offset_y),
        )

    def draw(
        self,
        screen: pg.Surface,
        cell_size: int,
        offset_x: int,
        offset_y: int,
    ) -> None:
        """Draw the drone in the screen

            Args:
                screen (Surface): Represent the screen
                cell_size (int): the size of the box's zone
                offset_x (int): Represent the x mouse pos
                offset_y (int): Represent the y mouse pos
        """
        screen_x, screen_y = self.screen_pos(cell_size, offset_x, offset_y)

        size = max(10, int(cell_size * 0.5))

        if self._scaled_image is None or size != self._scaled_size:
            self._scaled_image = pg.transform.smoothscale(
                self.image, (size, size)
            )
            self._scaled_size = size

        rect = self._scaled_image.get_rect(
            center=(
                int(screen_x), int(screen_y)
            )
        )

        screen.blit(self._scaled_image, rect)
