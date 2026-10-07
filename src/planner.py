import heapq
from typing import Any


from src.zone import Zone

from .color import color_rgb
from .utils import Utils

INF = float("inf")

Action = tuple[float, float] | None


class Planner:
    def __init__(
        self,
        zones: list[Zone],
        connections: list[Any],
        nb_drones: int,
    ) -> None:
        self.zones = {z.name: z for z in zones}
        self.start = next((z for z in zones if z.is_start), None)
        self.end = next((z for z in zones if z.is_end), None)
        self.nb_drones = nb_drones
        self.horizon = 4 * (len(zones) + nb_drones)
        self.loading = True
        self.adj: dict[str, list[tuple[Zone, frozenset[str], int, int]]] = {
            z.name: [] for z in zones
        }
        for conn in connections:
            a, b = conn.zone1, conn.zone2
            key = frozenset((a.name, b.name))
            cap = int(conn.metadata.get("max_link_drone", 1))
            for src, dst in ((a, b), (b, a)):
                kind = self._type(dst)
                if kind == "blocked":
                    continue
                cost = 2 if kind == "restricted" else 1
                self.adj[src.name].append((dst, key, cap, cost))

        self.zone_use: dict[tuple[str, int], int] = {}
        self.link_use: dict[tuple[frozenset[str], int], int] = {}
        self.timeline: dict[int, list[tuple[str, str]]]

    def get_loading(self) -> bool:
        return self.loading

    def set_loading(self, loading: bool) -> None:
        self.loading = loading

    @staticmethod
    def _type(zone: Zone) -> str:
        return str(getattr(zone, "type", zone)).lower()

    @staticmethod
    def _capacity(zone: Zone) -> float:
        if zone.is_start or zone.is_end:
            return INF
        return zone.max_drones

    def plan_all(self) -> list[list[Action]]:
        plans: list[list[Action]] = []
        paths: list[list[tuple[str, int]]] = []
        for i in range(self.nb_drones):
            path = self._find_path()
            if path is None:
                print(f"No path found for drone {i + 1}")
                plans.append([])
                continue
            self._reserve(path)
            paths.append(path)
            plans.append(self._to_actions(path))

        cpt = 0
        goal_cpt = 0
        while goal_cpt != self.nb_drones:
            for y in range(len(paths)):
                if cpt + 1 >= len(paths[y]):
                    continue

                current_zone, current_turn = paths[y][cpt]
                next_zone, next_turn = paths[y][cpt + 1]

                if current_zone == next_zone:
                    continue

                if self.end:
                    if next_zone == self.end.name:
                        goal_cpt += 1

                if next_turn - current_turn != 1:
                    Utils.print_rgb(
                        f"D{y + 1}-{current_zone}-{next_zone}",
                        color_rgb[str(self.zones[next_zone].color).upper()],
                    )
                else:
                    Utils.print_rgb(
                        f"D{y + 1}-{next_zone}",
                        color_rgb[str(self.zones[next_zone].color).upper()],
                    )
            print()
            cpt += 1

        self.loading = False
        return plans

    def _find_path(self) -> list[tuple[str, int]] | None:
        if self.start is None or self.end is None:
            return None

        first = (self.start.name, 0)
        dist: dict[tuple[str, int], int] = {first: 0}
        parent: dict[tuple[str, int], tuple[str, int] | None] = {first: None}
        heap: list[tuple[int, int, str]] = [(0, 0, self.start.name)]
        done: set[tuple[str, int]] = set()
        i = 0
        while heap:
            t, pen, name = heapq.heappop(heap)
            state = (name, t)
            if state in done:
                continue
            done.add(state)

            if name == self.end.name:
                path = []
                cur: tuple[str, int] | None = state
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()
                return path

            if t >= self.horizon:
                continue

            zone = self.zones[name]

            if self.zone_use.get((name, t + 1), 0) < \
                    float(self._capacity(zone)):
                self._push(state, (name, t + 1), pen, dist, parent, heap)

            for dst, key, link_cap, cost in self.adj[name]:
                arrive = t + cost
                if any(
                    self.link_use.get((key, t + k), 0) >= link_cap
                    for k in range(1, cost + 1)
                ):
                    continue

                if self.zone_use.get((dst.name, arrive), 0) >= float(
                    self._capacity(dst)
                ):
                    continue
                new_pen = pen + (0 if self._type(dst) == "priority" else 1)
                self._push(
                    state, (dst.name, arrive),
                    new_pen, dist, parent, heap
                )
            i += 1
        return None

    @staticmethod
    def _push(
                cur: tuple[str, int],
                nxt: tuple[str, int],
                pen: int, dist: dict[tuple[str, int], int],
                parent: dict[tuple[str, int], tuple[str, int] | None],
                heap: list[tuple[int, int, str]]
            ) -> None:
        if pen < dist.get(nxt, INF):
            dist[nxt] = pen
            parent[nxt] = cur
            heapq.heappush(heap, (nxt[1], pen, nxt[0]))

    def _reserve(self, path: list[tuple[str, int]]) -> None:
        for name, t in path:
            if self._capacity(self.zones[name]) != INF:
                self.zone_use[(name, t)] = self.zone_use.get((name, t), 0) + 1

        for (a, ta), (b, tb) in zip(path, path[1:]):
            if a == b:
                continue
            key = frozenset((a, b))
            for k in range(1, tb - ta + 1):
                self.link_use[(key, ta + k)] = self.link_use.get(
                    (key, ta + k), 0) + 1

    def _to_actions(self, path: list[tuple[str, int]]) -> list[Action]:
        actions: list[Action] = []
        for (a, ta), (b, tb) in zip(path, path[1:]):
            if a == b:
                actions.append(None)
                continue
            za, zb = self.zones[a], self.zones[b]
            if tb - ta == 1:
                actions.append((float(zb.x), float(zb.y)))
            else:
                actions.append(((za.x + zb.x) / 2, (za.y + zb.y) / 2))
                actions.append((float(zb.x), float(zb.y)))
        return actions
