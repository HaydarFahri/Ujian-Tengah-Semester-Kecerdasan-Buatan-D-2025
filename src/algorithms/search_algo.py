import heapq
from collections import deque
from typing import List, Tuple, Optional

class SearchEngine:
    """
    Mesin pencari jalur graph (Pathfinding Engine).
    Mendukung algoritma Blind Search (BFS, DFS) dan Heuristic Search (A*).
    """
    def __init__(self, graph: dict, heuristics: dict):
        self.graph = graph
        self.heuristics = heuristics

    def bfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], List[str]]:
        """
        Breadth-First Search (BFS).
        Menjelajah level demi level menggunakan Queue (FIFO).
        :return: (Jalur Terpendek secara hops, Log Kunjungan)
        """
        queue = deque([(start, [start])])
        visited = set()
        log = []  # Menyimpan urutan node yang dieksplorasi

        while queue:
            node, path = queue.popleft()
            
            if node not in log:
                log.append(node)
            
            if node == goal:
                return path, log
            
            visited.add(node)
            
            # Ambil tetangga
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None, log

    def dfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], List[str]]:
        """
        Depth-First Search (DFS).
        Menjelajah kedalaman cabang menggunakan Stack (LIFO).
        :return: (Jalur ditempuh, Log Kunjungan)
        """
        stack = [(start, [start])]
        visited = set()
        log = []

        while stack:
            node, path = stack.pop()
            
            if node not in log:
                log.append(node)
            
            if node == goal:
                return path, log
            
            if node not in visited:
                visited.add(node)
                # Reverse urutan agar DFS mengunjungi dari kiri ke kanan secara visual
                neighbors = self.graph.get(node, [])
                for neighbor, _ in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))
        
        return None, log

    def a_star(self, start: str, goal: str) -> Tuple[Optional[List[str]], List[str], float]:
        """
        A* (A-Star) Search Algorithm.
        Menggunakan fungsi evaluasi: f(n) = g(n) + h(n).
        :return: (Jalur Optimal, Log Kunjungan, Total Cost)
        """
        # Priority Queue: (f_score, current_node, path, g_score)
        pq = [(0, start, [start], 0)] 
        visited = set()
        log = []

        while pq:
            # Pop node dengan f_score terendah
            f, node, path, g = heapq.heappop(pq)
            
            log.append(f"{node} (f={f:.1f})")
            
            if node == goal:
                return path, log, g
            
            visited.add(node)
            
            for neighbor, cost in self.graph.get(node, []):
                new_g = g + cost
                # Ambil nilai heuristik (h), default 0 jika tidak ada
                h = self.heuristics.get(neighbor, 0)
                new_f = new_g + h
                
                heapq.heappush(pq, (new_f, neighbor, path + [neighbor], new_g))
                
        return None, log, float('inf')