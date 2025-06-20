import heapq
from typing import List, Tuple, Optional

class PathFinder:
    def __init__(self, layout: List[List[int]]):
        self.layout = layout
        self.rows = len(layout)
        self.cols = len(layout[0]) if layout else 0
        
    def is_walkable(self, row: int, col: int) -> bool:
        """Check if a position is walkable (not a wall or shelf)"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = self.layout[row][col]
            # 0 = walkway, 9 = entrance/exit are walkable
            return cell in [0, 9]
        return False
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get walkable neighboring positions"""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def find_shortest_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """A* pathfinding algorithm"""
        if not self.is_walkable(start[0], start[1]) or not self.is_walkable(goal[0], goal[1]):
            return None
        
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]
            
            for neighbor in self.get_neighbors(current[0], current[1]):
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None  # No path found
    
    def find_nearest_product(self, start: Tuple[int, int], product_positions: List[Tuple[int, int]]) -> Optional[Tuple[Tuple[int, int], List[Tuple[int, int]]]]:
        """Find the nearest product and return its position and path"""
        shortest_path = None
        nearest_product = None
        min_distance = float('inf')
        
        for product_pos in product_positions:
            path = self.find_shortest_path(start, product_pos)
            if path and len(path) < min_distance:
                min_distance = len(path)
                shortest_path = path
                nearest_product = product_pos
        
        if shortest_path and nearest_product:
            return nearest_product, shortest_path
        return None
