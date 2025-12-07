import sqlite3
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import os
from backend import yolotanim 

# Test klasörü sabit adresi
TEST_FOLDER = "test_images" 

def connect_db():
    return sqlite3.connect('backend/nutrition_data.db')

def get_food_nutrition(food_name):
    bag = connect_db()
    b = bag.cursor()
    b.execute("SELECT calories, protein, carbs, fat FROM foods WHERE name=?", (food_name,))
    result = b.fetchone()
    bag.close()
    return result

def analyze_food_image(image_path="test_images/salad.jpg"):
    """
    YOLOv8 ile yemek tespiti yapar ve SABİT besin değerlerini döndürür.
    Gramaj tahmini kaldırıldı - 100g bazında standart değerler kullanılıyor.
    """
    abs_image_path = os.path.join(os.getcwd(), image_path) 
    
    model = yolotanim.load_model()
    if model is None:
        return pd.DataFrame([{'HATA': "Model yuklenemedi."}])

    print(f"Tespit basliyor: {abs_image_path}")
    
    if not os.path.exists(abs_image_path):
        return pd.DataFrame([{'HATA': f"Test resmi bulunamadi: '{abs_image_path}'"}])

    results = model.predict(source=abs_image_path, conf=0.5, verbose=False)
    analysis_results = []

    for r in results:
        classes = r.boxes.cls.cpu().numpy()
        names = r.names
        
        for cls in classes:
            food_name = names[int(cls)]
            nutrition = get_food_nutrition(food_name)

            if nutrition:
                # Sabit değerler (100g bazında) - Gramaj tahmini YOK
                cal_per_100g, prot_per_100g, carb_per_100g, fat_per_100g = nutrition
                
                analysis_results.append({
                    'Yemek': food_name,
                    'Kalori': int(cal_per_100g),
                    'Protein': round(prot_per_100g, 1),
                    'Karbonhidrat': round(carb_per_100g, 1),
                    'Yağ': round(fat_per_100g, 1)
                })
            else:
                analysis_results.append({
                    'Yemek': food_name, 
                    'Kalori': 'Veri Eksik',
                    'Protein': 0,
                    'Karbonhidrat': 0,
                    'Yağ': 0
                })

    return pd.DataFrame(analysis_results)

if __name__ == "__main__":
    print(analyze_food_image(image_path="test_images/salad.jpg"))