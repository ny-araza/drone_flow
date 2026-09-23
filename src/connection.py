from .zone import Zone
from typing import Any

class Connection:
    def __init__(self, zone1: Zone, zone2: Zone, metadata: dict[str, int]):
        self.zone1 = zone1
        self.zone2 = zone2
        self.metadata = metadata

