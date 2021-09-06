# Graph-Traversal-Algorithms-Visualizer
Interactive application for visualizing and comparing four of the main graph traversal algorithms:
- Depth FS
- Breadth FS
- Greedy FS
- A*


## Understanding the Visualizer
When first launched, you will see an empty grid of tiles, with a green tile at the upper left corner, and a red tile at the bottom right corner.
The green tile is the **origin**, while the red tile is the **target**.

The algorithm you select will traverse the grid from the origin (*no diagonal moves allowed*), in search of the target.

You can add walls which will be represented by a dark blue color. The algorithm cannot move into walls.


Once you run the algorithm, you will see three more different types of tiles:
- **Orange**: The orange tile represents the current tile the algorithm is on. You can think of this as the head of the algorithm, from which it may move to another tile or see neighboring tiles.
- **Light Blue**: Light blue tiles represent tiles that the algorithm has already seen or visited. There is no need to visit these again. It can be useful to compare the amount of blue tiles one algorithm has, compared to another. The less blue tiles the faster it will usually be.
- **Light Green**: Light green tiles represent the path the algorithm has taken to reach the orange tile. You may see the length of the path sometimes decrease, as some algorithms like DFS and GFS backtrack, meaning they go back from where they came from if they find a dead-end.  


## Utility
- Left-click to draw walls, right-click to remove them.
- Click and drag origin and target tile to change their position.
- Buttons:
  - The top row of buttons are the algorithms you can select. 
  - The *Clear* button will erase all tiles, except for the origin and target.
  - The *Generate maze* button will create a randomized maze that has multiple different solutions from origin to target.
  - The *Fast / Slow* buttons will select the speed at which the algorithm is visualized. You can change the speed at any time.


## Algorithms
### [Depth First Search](https://en.wikipedia.org/wiki/Depth-first_search)
Depth First Search (**DFS**) is an uninformed algorithm, which means that it does not know where the target tile is. As the name implies, DFS explores in an arbitrary direction until it reaches a dead-end, at which point it returns to the last point it made a decision and explores another path. This algorithm is very good for when you do not know where the target is, but you expect if to be far away and you do not care about finding the shortest path.

### [Breadth First Search](https://en.wikipedia.org/wiki/Breadth-first_search)
Breadth First Search (**BFS**) is also an uninformed algorithm. Contrary to DFS, BFS searches first all tiles at a certain depth, before moving on to the tiles that are farther from the origin. Thanks to this, BFS will allways find the shortest path, but it usually is slower than DFS, especially when there are multiple solutions or the target is expected to be far away.

### [Greedy First Search](https://en.wikipedia.org/wiki/Best-first_search)
Greedy First Search (**GFS**), also known as Best First Search, is an informed search algorithm, which means it knows where the target tile is. It behaves in a similar way to DFS in the sense it explores a path completely, before going back if it is a dead end. However, it can make better decisions regarding what path to explore as it can calculate the minimum distance (*heuristic fucntion used was manhattan distance*) that each decision would lead to, and then chooses the shortest one. It is very fast, but does not assure the shortest path.

### [A Star](https://en.wikipedia.org/wiki/A*_search_algorithm)
A Star, or A*, is considered the best informed search algorithm that assures to find the shortest path. When the *cost* of traversing tiles is the same every for all tiles, such as in our case, A* will behave exactly the same as another algorithm named [Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm). A* is somewhat similar to BFS, but instead of searching by depth, it searches by exploring the path or paths that have the possibility of being the shortest path. This is calculated by adding the length of the path and the minimum distance to the target from there, the lower the number the shorter the path may be.
