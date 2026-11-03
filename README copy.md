*This project has been created as part of the 42 curriculum by ny-araza*

# DESCRIPTION

The "fly-in" project involves simulating drones to find the shortest path from point A to point B. The graph is weighted, A default zone costs 1 to travel to from a given point, whereas a restricted zone costs 2. Regarding connections, a connection may limit the number of drones passing through it.

### Algorithm choices and implementation strategy
Here, a weighted graph is used, so Dijkstra's algorithm is more suitable.
For the implementation, I used objects to store connections, drones, and zones, in order to better manage them and adhere to the problem's constraints during pathfinding.

For the graphical display, I used Pygame.

**Dijkstra's algorithm:**

I have stored the possible movements of a drone in an array on the heap. Like this **heap: list[tuple[int, int, str]]**. For the first value its the turn count, the second either 1 or 0, 0 if it has priority, and 1 otherwise and the last is the name of the destination zone.

A heap list rearranges the list by always placing the smallest element at the top (as the first element).

For zone-type management, I store the number of drones during a given turn *t* in a dictionary, and I do the same for the connection.

To construct a drone's path, I store each movement in a dictionary, using the current zone as the key and the destination as the value.

### Complexity of the algorithm
My algo have a *O( n T d C Log ( n T d ) )* <br>
With:
<ul>
    <li>n: number of drone</li>
    <li>T: number total of possible turn to reach the endzone</li>
    <li>d: number of neighbors in a zone</li>
    <li>heappush/heappop: O(Log(n T d))</li>
</ul>

### Optimisation
Before, I used a simple list to store a drone's possible movements; each time, I would call a sort function to find the minimum value, which was not efficient in terms of performance.
I then replaced it with a heap—a structure that sorts itself upon every insertion (push). It places the smallest element at the top of the tree, making it easy to retrieve the minimum and resulting in faster execution.

### Visual representation features

For the graphical representation, I have included the number of turn per drone,
the minimum number of turn across all drones,
and the total number of turn required for all drones to reach their destination.
The user can also display and hide the zone's name and drone's name.

The user can zoom and move the map using <+> <-> keys or using the moulette. This ensures the map is displayed properly when it fills the entire screen.
It also ensures that drone names are displayed correctly, even when zones are too close together and the names would otherwise overlap.

User can display or hide the name of each hub using < p >

### Example program's functionnality

#### Input
This is a map file example input.txt
```txt
nb_drones: 1
start_hub: start 0 0 [color=green max_drones=2]
hub: waypoint1 1 0 [color=blue zone=blocked]
hub: waypoint2 2 0 [color=yellow zone=priority]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint2-start
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

##### parsing:
The coordinates are limited by the size of the window.
To avoid excessively long wait times, the total number of allowed drones is limited at 100.

#### Output
This is an expected output shows in the terminal
```bash
D1-waypoint2 
D1-goal 
```
At t1, the drone moves toward waypoint 1.
At t2, it moves toward the goal.

# INSTRUCTION

```bash
    make
    # install the project dependencies then run it
```

```bash
    make install
    # Install the project dependencies
```

```bash
    make run
    # run the program with the default map (01_linear_path.txt)
```

```bash
    make run-folder ARGS=maps # the folder maps
    # run the program with the maps folder
```

```bash
    make lint
    # Check the mypy and the flake8
```

```bash
    make lint-strict
    # Check the mypy in strict-mode
```

```bash
    make clean
    # delete all __pycache__ folder
```

```bash
    make fclean
    # Reset all dependencies
```

# RESSOURCES

### Articles and tutorials
<ul>
    <li>
        <a href="https://www.pygame.org/docs/">Learn pygame</a>
    </li>
    <li>
        <a href="https://en.wikipedia.org/wiki/Dijkstra's_algorithm">Dijkstra's algorithm</a>
    </li>
    <li>
        <a href="https://coddy.tech/visualize/graphs/dijkstras-algorithm">Dijkstra vizualisation</a>
    </li>
</ul>

### AI using
<ul>
    <li>Help me for the comprehension of dijkstra's algorithm</li>
    <li>Help me for debuging pygame</li>
</ul>


#############

Ce n’est pas la capacité start → waypoint1 qui bloque, il y a deux causes.

1. Ta map limite le passage à 1 drone par tour

waypoint2 n’a pas de max_drones, donc il prend probablement la valeur par défaut (1). Même chose pour les connexions waypoint1-waypoint2 et waypoint2-goal, dont la capacité par défaut est 1. Au maximum, un drone entre donc dans waypoint2 à chaque tour. Pour que tout avance en groupe, il faut :
```bash
hub: waypoint2 2 0 [max_drones=7]
connection: waypoint1-waypoint2 [max_link_capacity=7]
connection: waypoint2-goal [max_link_capacity=7]
```
2. Le Dijkstra attend au départ au lieu d’attendre dans waypoint1

Même avec le goulot en 1 drone par tour, ton attente devrait se faire dans waypoint1, comme tu le décris. Ici, le drone 2 reste sur start puis entre dans waypoint1 plus tard, d’où l’effet « un par un ».

La cause est dans _push :

```python
if pen < dist.get(nxt, INF):
```
Le comparateur est strict (<). Pour l’état (waypoint1, 2), il y a deux chemins de même coût :

A : attendre à start au tour 1, puis aller à waypoint1.
B : aller à waypoint1 au tour 1, puis y attendre.

Le heap est trié par (t, pen, name) et (start, 1) a pen=0, donc il sort avant (waypoint1, 1). A est poussé en premier, et B, à égalité, ne le remplace pas à cause du < strict. Le drone attend donc sur start, qui a une capacité infinie.

Correction : en cas d’égalité, préférer le parent qui est une attente (même zone). Le drone avance alors le plus tôt possible et n’attend que dans la dernière zone atteinte :

```python
@staticmethod
def _push(cur, nxt, pen, dist, parent, heap) -> None:
    old = dist.get(nxt, INF)
    better = pen < old
    # à égalité, préférer "avancer d'abord, attendre ensuite"
    tie_wait = pen == old and cur[0] == nxt[0]
    if better or tie_wait:
        dist[nxt] = pen
        parent[nxt] = cur
        heapq.heappush(heap, (nxt[1], pen, nxt[0]))
```
Avec ça, et la map corrigée, les 7 drones vont sur waypoint1 au tour 1. Si waypoint2 reste limité à 1, ils attendent dans waypoint1 (capacité 7) et passent un par un, sans bloquer start.

Le temps total est le même dans les deux cas. Seul l’ordre des déplacements change, mais c’est plus fidèle à ce qu’on attend visuellement.