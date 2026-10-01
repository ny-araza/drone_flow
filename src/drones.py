class Drone:
    def __init__(self, x: int, y: int, image: str) -> None:
        self.x = x
        self.y = y
        self.turn = 0
        self.checkpoint = False
        self.path = []
        self.image = image

    def mouve(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy
