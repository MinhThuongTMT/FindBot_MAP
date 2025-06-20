import heapq
import math
from typing import List, Tuple, Optional, Dict

class EnhancedPathFinder:
    def __init__(self, layout: List[List[int]]):
        self.layout = layout
        self.rows = len(layout)
        self.cols = len(layout[0]) if layout else 0
        self.path_history = []
        
    def is_walkable(self, row: int, col: int) -> bool:
        """Check if a position is walkable (not a wall or shelf)"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            cell = self.layout[row][col]
            # 0 = walkway, 9 = entrance/exit are walkable
            return cell in [0, 9]
        return False
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get walkable neighboring positions - only cardinal directions"""
        neighbors = []
        # Only 4-directional movement (no diagonals)
        directions = [
            (0, 1),   # right
            (1, 0),   # down
            (0, -1),  # left
            (-1, 0)   # up
        ]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_walkable(new_row, new_col):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def heuristic(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Manhattan distance heuristic for 4-directional movement"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def find_shortest_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """A* pathfinding algorithm for shortest path"""
        if not self.is_walkable(start[0], start[1]) or not self.is_walkable(goal[0], goal[1]):
            return None
        
        if start == goal:
            return [start]
        
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
                path.reverse()
                
                # Store in history
                self.path_history.append({
                    'start': start,
                    'goal': goal,
                    'path': path,
                    'length': len(path)
                })
                
                return path
            
            for neighbor in self.get_neighbors(current[0], current[1]):
                tentative_g_score = g_score[current] + 1  # Each step costs 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return None  # No path found
    
    def find_nearest_shelf_access(self, start: Tuple[int, int], shelf_positions: List[Tuple[int, int]]) -> Optional[Tuple[Tuple[int, int], List[Tuple[int, int]], float]]:
        """Find the nearest accessible point around a shelf using shortest path"""
        best_path = None
        best_target = None
        min_distance = float('inf')
        
        # For each shelf position, find nearby walkable positions
        for shelf_pos in shelf_positions:
            row, col = shelf_pos
            
            # Check positions around the shelf (4 cardinal directions)
            adjacent_positions = [
                (row - 1, col),  # up
                (row + 1, col),  # down
                (row, col - 1),  # left
                (row, col + 1)   # right
            ]
            
            for target_row, target_col in adjacent_positions:
                if self.is_walkable(target_row, target_col):
                    path = self.find_shortest_path(start, (target_row, target_col))
                    if path:
                        distance = len(path) - 1  # Number of steps
                        
                        if distance < min_distance:
                            min_distance = distance
                            best_path = path
                            best_target = (target_row, target_col)
        
        if best_path and best_target:
            return best_target, best_path, min_distance
        return None
    
    def get_path_history(self) -> List[Dict]:
        """Get pathfinding history"""
        return self.path_history
    
    def clear_history(self):
        """Clear pathfinding history"""
        self.path_history.clear()
