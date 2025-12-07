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

def calculate_grammage(box_area, area_threshold=50000, reference_gram=100):
    if box_area <= 0:
        return 0
    grammage = (box_area / area_threshold) * reference_gram
    return max(10, round(grammage))


def analyze_food_image(image_path="test_images/salad.jpg"):
    
    # --- DÜZELTİLDİ: 'backend' klasörünü yola ekledik. ---
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
        boxes = r.boxes.xyxy.cpu().numpy()
        classes = r.boxes.cls.cpu().numpy()
        names = r.names
        
        for box, cls in zip(boxes, classes):
            x1, y1, x2, y2 = box
            box_area = (x2 - x1) * (y2 - y1)
            
            food_name = names[int(cls)]
            
            grammage = calculate_grammage(box_area)
            nutrition = get_food_nutrition(food_name)

            if nutrition:
                cal_per_100g, prot_per_100g, carb_per_100g, fat_per_100g = nutrition
                
                multiplier = grammage / 100
                total_calories = int(cal_per_100g * multiplier)
                
                analysis_results.append({
                    'Yemek': food_name,
                    'Gramaj': f"{grammage}g",
                    'Kalori': total_calories,
                    'Protein': round(prot_per_100g * multiplier, 1),
                    'Karbonhidrat': round(carb_per_100g * multiplier, 1)
                })
            else:
                analysis_results.append({'Yemek': food_name, 'Gramaj': 'Bilinmiyor', 'Kalori': 'Veri Eksik'})

    return pd.DataFrame(analysis_results)

if __name__ == "__main__":
    print(analyze_food_image(image_path="test_images/salad.jpg"))