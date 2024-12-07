import pandas as pd
import numpy as np

# Türkiye'deki ürünler ve özelliklerine uygun değer aralıkları
products = {
   "Buğday": {
        "Soil Texture (Sand %)": (30, 50),
        "pH": (6.0, 7.5),
        "Soil Depth (cm)": (80, 150),
        "Nitrogen (N) (%)": (0.8, 1.2),
        "Phosphorus (P) (ppm)": (15, 30),
        "Potassium (K) (ppm)": (100, 250),
        "Soil Moisture Content (%)": (10, 20)
    },
    "Arpa": {
        "Soil Texture (Sand %)": (30, 60),
        "pH": (6.0, 7.5),
        "Soil Depth (cm)": (70, 140),
        "Nitrogen (N) (%)": (0.6, 1.0),
        "Phosphorus (P) (ppm)": (10, 25),
        "Potassium (K) (ppm)": (80, 200),
        "Soil Moisture Content (%)": (8, 18)
    },
    "Zeytin": {
        "Soil Texture (Sand %)": (50, 70),
        "pH": (7.0, 8.0),
        "Soil Depth (cm)": (100, 200),
        "Nitrogen (N) (%)": (0.5, 1.0),
        "Phosphorus (P) (ppm)": (10, 25),
        "Potassium (K) (ppm)": (150, 300),
        "Soil Moisture Content (%)": (5, 15)
    },
    "Fındık": {
        "Soil Texture (Sand %)": (40, 60),
        "pH": (5.5, 6.5),
        "Soil Depth (cm)": (100, 150),
        "Nitrogen (N) (%)": (0.8, 1.5),
        "Phosphorus (P) (ppm)": (20, 40),
        "Potassium (K) (ppm)": (100, 200),
        "Soil Moisture Content (%)": (15, 30)
    },
    "Pamuk": {
        "Soil Texture (Sand %)": (50, 80),
        "pH": (7.0, 8.0),
        "Soil Depth (cm)": (100, 180),
        "Nitrogen (N) (%)": (0.7, 1.2),
        "Phosphorus (P) (ppm)": (10, 30),
        "Potassium (K) (ppm)": (150, 300),
        "Soil Moisture Content (%)": (10, 25)
    },
    "Domates": {
        "Soil Texture (Sand %)": (40, 70),
        "pH": (6.5, 7.5),
        "Soil Depth (cm)": (50, 120),
        "Nitrogen (N) (%)": (1.0, 2.0),
        "Phosphorus (P) (ppm)": (15, 40),
        "Potassium (K) (ppm)": (200, 400),
        "Soil Moisture Content (%)": (15, 30)
    },
    "Çay": {
        "Soil Texture (Sand %)": (30, 50),
        "pH": (4.5, 6.0),
        "Soil Depth (cm)": (70, 150),
        "Nitrogen (N) (%)": (1.0, 1.5),
        "Phosphorus (P) (ppm)": (10, 25),
        "Potassium (K) (ppm)": (80, 200),
        "Soil Moisture Content (%)": (20, 40)
    },
    "Üzüm": {
        "Soil Texture (Sand %)": (40, 60),
        "pH": (6.0, 7.5),
        "Soil Depth (cm)": (70, 150),
        "Nitrogen (N) (%)": (0.5, 1.0),
        "Phosphorus (P) (ppm)": (15, 30),
        "Potassium (K) (ppm)": (150, 300),
        "Soil Moisture Content (%)": (10, 25)
    },
    "Kayısı": {
        "Soil Texture (Sand %)": (40, 60),
        "pH": (6.5, 7.5),
        "Soil Depth (cm)": (100, 180),
        "Nitrogen (N) (%)": (0.7, 1.2),
        "Phosphorus (P) (ppm)": (10, 30),
        "Potassium (K) (ppm)": (100, 250),
        "Soil Moisture Content (%)": (8, 20)
    }
}

# Her ürün için veri seti oluşturma
for product, properties in products.items():
    data = {}
    for prop, (low, high) in properties.items():
        data[prop] = np.random.uniform(low, high, 100)  # 100 satır veri oluştur
    df = pd.DataFrame(data)
    
    # CSV olarak kaydet
    file_name = f"{product}_soil_properties.csv"
    df.to_csv(file_name, index=False)
    print(f"{product} için veri seti oluşturuldu ve '{file_name}' olarak kaydedildi.")
