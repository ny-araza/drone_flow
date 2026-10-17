from zone import Zone


class Connection:
    """Represent the connection of two zone

        Attributes:
            zone1 (Zone): the source zone
            zone2 (Zone): the destination zone
            metadata (dict[str, int]): the metadata for zone (max_link_capacity)
    """
    def __init__(self, zone1: Zone, zone2: Zone, metadata: dict[str, int]):
        """Contructor for Connection Class

            Args:
                zone1 (Zone): the source zone
                zone2 (Zone): the destination zone
                metadata (dict[str, int]): the metadata for zone (max_link_capacity)
        """
        self.zone1 = zone1
        self.zone2 = zone2
        self.metadata = metadata
