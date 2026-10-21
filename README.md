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
Before, I use a simple list to store the possibility of move for one drone. This 

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
