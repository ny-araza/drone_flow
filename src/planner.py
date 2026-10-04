from __future__ import annotations

import heapq
from sys import intern
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.zone import Zone

INF = float("inf")

# Une action = position cible (x, y) pour un tour, ou None si le drone attend
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
        self.horizon = 4 * (len(zones) + nb_drones) + 10

        # adj[nom] = [(zone_voisine, clé_connexion, capacité_connexion, coût)]
        self.adj: dict[str, list[tuple[Zone, frozenset, int, int]]] = {
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

        # Réservations : (nom_zone, t) -> nb drones, (clé_connexion, t) -> nb
        self.zone_use: dict[tuple[str, int], int] = {}
        self.link_use: dict[tuple[frozenset, int], int] = {}

    # ------------------------------------------------------------------
    @staticmethod
    def _type(zone: Zone) -> str:
        return str(getattr(zone.type, "value", zone.type)).lower()

    @staticmethod
    def _capacity(zone: Zone) -> float:
        if zone.is_start or zone.is_end:
            return INF
        return zone.max_drones

    # ------------------------------------------------------------------
    def plan_all(self) -> list[list[Action]]:
        plans: list[list[Action]] = []
        for i in range(self.nb_drones):
            path = self._find_path()
            if path is None:
                print(f"Aucun chemin valide pour le drone {i + 1}")
                plans.append([])
                continue
            self._reserve(path)
            plans.append(self._to_actions(path))
        return plans

    def _find_path(self) -> list[tuple[str, int]] | None:
        if self.start is None or self.end is None:
            return None

        first = (self.start.name, 0)
        dist: dict[tuple[str, int], int] = {first: 0}
        parent: dict[tuple[str, int], tuple[str, int] | None] = {first: None}
        heap: list[tuple[int, int, str]] = [(0, 0, self.start.name)]
        done: set[tuple[str, int]] = set()

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

            # Attendre sur place
            if self.zone_use.get((name, t + 1), 0) < float(self._capacity(zone)):
                self._push(state, (name, t + 1), pen, dist, parent, heap)

            # Se déplacer
            for dst, key, link_cap, cost in self.adj[name]:
                arrive = t + cost
                if any(
                    self.link_use.get((key, t + k), 0) >= link_cap
                    for k in range(1, cost + 1)
                ):
                    continue
                if self.zone_use.get((dst.name, arrive), 0) >= float(self._capacity(dst)):
                    continue
                new_pen = pen + (0 if self._type(dst) == "priority" else 1)
                self._push(state, (dst.name, arrive), new_pen, dist, parent, heap)

        return None

    @staticmethod
    def _push(cur, nxt, pen, dist, parent, heap) -> None:
        if pen < dist.get(nxt, INF):
            dist[nxt] = pen
            parent[nxt] = cur
            heapq.heappush(heap, (nxt[1], pen, nxt[0]))

    def _reserve(self, path: list[tuple[str, int]]) -> None:
        # Zones occupées à chaque instant entier
        for name, t in path:
            if self._capacity(self.zones[name]) != INF:
                self.zone_use[(name, t)] = self.zone_use.get((name, t), 0) + 1

        # Connexions utilisées pendant chaque tour de déplacement
        for (a, ta), (b, tb) in zip(path, path[1:]):
            if a == b:
                continue
            key = frozenset((a, b))
            for k in range(1, tb - ta + 1):
                self.link_use[(key, ta + k)] = self.link_use.get((key, ta + k), 0) + 1

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
                # Zone restreinte : mi-chemin au 1er tour, arrivée au 2e
                actions.append(((za.x + zb.x) / 2, (za.y + zb.y) / 2))
                actions.append((float(zb.x), float(zb.y)))
        return actions
