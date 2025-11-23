# Mengekspos Class utama agar bisa diakses langsung dari package algorithms
# Contoh pemakaian: from src.algorithms import TippingSystem, SearchEngine

from .fuzzy_logic import TippingSystem
from .search_algo import SearchEngine

__all__ = ['TippingSystem', 'SearchEngine']