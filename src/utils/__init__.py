"""
Utility Functions
Fungsi-fungsi bantuan umum yang bisa dipakai di mana saja.
"""

def format_percent(value):
    """Format angka desimal ke string persen (contoh: 0.4 -> 40%)"""
    return f"{value * 100:.0f}%"

def format_km(value):
    """Format jarak ke string KM"""
    return f"{value:.2f} KM"

def get_classification(tip_percent):
    """Klasifikasi teks berdasarkan persentase tip (Untuk UI Fuzzy)"""
    if tip_percent < 5.0:
        return "Rendah (Low)"
    elif tip_percent < 15.0:
        return "Sedang (Medium)"
    else:
        return "Tinggi (High)"