import numpy as np

class FuzzySet:
    """
    Representasi Himpunan Fuzzy dengan Kurva Segitiga.
    Mendukung operasi vektor (NumPy) dan menangani edge-cases (bahu kiri/kanan).
    """
    def __init__(self, name: str, a: float, b: float, c: float):
        """
        Inisialisasi Himpunan Fuzzy.
        :param name: Nama himpunan (contoh: 'Bad', 'Good')
        :param a: Batas bawah kiri
        :param b: Titik puncak (peak)
        :param c: Batas bawah kanan
        """
        self.name = name
        self.a = float(a)
        self.b = float(b)
        self.c = float(c)

    def membership(self, x):
        """
        Menghitung derajat keanggotaan (μ) untuk input x.
        :param x: Nilai input (scalar atau numpy array)
        :return: Nilai keanggotaan (0.0 - 1.0)
        """
        # Konversi ke array untuk kompatibilitas
        x = np.asarray(x)
        
        # 1. Handle Left Shoulder (Bahu Kiri Tegak - Contoh: Bad 0,0,5)
        if self.a == self.b:
            return np.where(x <= self.b, 1.0, np.maximum(0, (self.c - x) / (self.c - self.b)))
        
        # 2. Handle Right Shoulder (Bahu Kanan Tegak - Contoh: Excellent 5,10,10)
        elif self.b == self.c:
            return np.where(x >= self.b, 1.0, np.maximum(0, (x - self.a) / (self.b - self.a)))
        
        # 3. Normal Triangle (Segitiga Biasa)
        else:
            return np.maximum(0, np.minimum((x - self.a) / (self.b - self.a), 
                                            (self.c - x) / (self.c - self.b)))

class TippingSystem:
    """
    Sistem Pakar Penentuan Tip Restoran menggunakan Metode Mamdani.
    Logika: Min-Max Inference & Centroid Defuzzification.
    """
    def __init__(self):
        # Knowledge Base Initialization
        self.food = {
            "Bad": FuzzySet("Bad", 0, 0, 5),
            "Good": FuzzySet("Good", 5, 10, 10)
        }
        self.service = {
            "Poor": FuzzySet("Poor", 0, 0, 5),
            "Excellent": FuzzySet("Excellent", 5, 10, 10)
        }
        self.tip = {
            "Low": FuzzySet("Low", 0, 0, 10),
            "High": FuzzySet("High", 10, 20, 20)
        }

    def compute(self, food_val: float, service_val: float) -> dict:
        """
        Menjalankan proses inferensi fuzzy lengkap.
        
        Steps:
        1. Fuzzifikasi: Input Tegas -> Derajat Keanggotaan
        2. Inferensi: Evaluasi Rule (AND/OR) & Implikasi (MIN)
        3. Agregasi: Gabung Kurva Output (MAX)
        4. Defuzzifikasi: Hitung Centroid (Titik Pusat)

        :return: Dictionary berisi hasil centroid dan data plotting.
        """
        # 1. Fuzzification (Scalar Input -> Membership Degree)
        # Kita bungkus input jadi list [val] agar kompatibel dengan fungsi membership
        mu_food = {k: v.membership([food_val])[0] for k, v in self.food.items()}
        mu_svc = {k: v.membership([service_val])[0] for k, v in self.service.items()}

        # 2. Inference (Rule Evaluation)
        # Rule 1: IF Service Poor OR Food Bad THEN Tip Low
        alpha1 = max(mu_svc["Poor"], mu_food["Bad"]) 
        
        # Rule 2: IF Service Excellent AND Food Good THEN Tip High
        alpha2 = min(mu_svc["Excellent"], mu_food["Good"]) 

        # 3. Defuzzification (Vectorized Centroid Method)
        # Membuat domain sampling (x axis) dari 0 sampai 20 dengan resolusi tinggi
        x_domain = np.linspace(0, 20, 500)
        
        # Generate kurva dasar output
        tip_low_curve = self.tip["Low"].membership(x_domain)
        tip_high_curve = self.tip["High"].membership(x_domain)
        
        # Implikasi (Potong kurva setinggi alpha)
        y_low = np.fmin(alpha1, tip_low_curve)
        y_high = np.fmin(alpha2, tip_high_curve)
        
        # Agregasi (Gabungkan semua area hasil potongan)
        y_agg = np.fmax(y_low, y_high)

        # Hitung Centroid: Sum(x * y) / Sum(y)
        numerator = np.sum(x_domain * y_agg)
        denominator = np.sum(y_agg)
        
        centroid = numerator / denominator if denominator != 0 else 0

        return {
            "centroid": centroid,
            "alpha": [alpha1, alpha2],
            "plot_data": (x_domain, y_low, y_high, y_agg)
        }