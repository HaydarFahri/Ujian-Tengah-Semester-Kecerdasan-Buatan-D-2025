"""
Unit Testing.
Menjalankan pengujian otomatis untuk memastikan logika Fuzzy dan Searching berjalan benar.
"""
import unittest
import numpy as np
from src.algorithms.fuzzy_logic import TippingSystem
from src.algorithms.search_algo import SearchEngine
from data.graph_repository import ROMANIA_MAP, HEURISTICS

class TestNexusAI(unittest.TestCase):
    
    def setUp(self):
        """Inisialisasi sebelum setiap test."""
        self.fuzzy = TippingSystem()
        # Gunakan peta Romania asli untuk testing standar
        self.search = SearchEngine(ROMANIA_MAP, HEURISTICS)

    def test_fuzzy_case_soal(self):
        """Test Kasus Soal Ujian: Food=7, Service=3"""
        print("\n🧪 Testing Fuzzy Logic (Food=7, Service=3)...")
        result = self.fuzzy.compute(7, 3)
        centroid = result['centroid']
        
        # Kita tahu hasil manualnya sekitar 4.08%
        # Kita toleransi perbedaan desimal (delta)
        self.assertAlmostEqual(centroid, 4.08, delta=0.5)
        print(f"   -> Hasil: {centroid:.4f}% (Valid ✅)")

    def test_fuzzy_best_case(self):
        """Test Kasus Sempurna: Food=10, Service=10 -> Tip Tinggi"""
        print("🧪 Testing Fuzzy Logic (Best Case)...")
        result = self.fuzzy.compute(10, 10)
        # Tip harusnya tinggi (>15%)
        self.assertGreater(result['centroid'], 15.0)
        print(f"   -> Hasil: {result['centroid']:.4f}% (Valid ✅)")

    def test_bfs_path(self):
        """Test BFS Arad -> Bucharest"""
        print("🧪 Testing BFS (Arad -> Bucharest)...")
        path, log = self.search.bfs('Arad', 'Bucharest')
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 'Arad')
        self.assertEqual(path[-1], 'Bucharest')
        print(f"   -> Jalur: {path} (Valid ✅)")

    def test_astar_optimality(self):
        """Test A* harus lebih efisien/sama cost-nya dibanding BFS"""
        print("🧪 Testing A* Optimality...")
        # Hitung manual cost BFS (jika lewat Sibiu-Fagaras)
        # Arad-Sibiu(140) + Sibiu-Fagaras(99) + Fagaras-Bucharest(211) = 450
        
        path_astar, log, cost_astar = self.search.a_star('Arad', 'Bucharest')
        
        # Cost A* (lewat Pitesti) harusnya 418
        self.assertTrue(cost_astar <= 450)
        print(f"   -> Cost A*: {cost_astar} (Valid ✅)")

if __name__ == '__main__':
    unittest.main()