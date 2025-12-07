# NOT: Bu dosya eski simülasyon scriptidir.
# Güncel simülasyon fonksiyonu için backend/database.py içindeki 
# generate_7_day_logs_for_100_users() fonksiyonunu kullanın.


import sqlite3
import random
from datetime import datetime, timedelta

def connect_db():
    return sqlite3.connect('backend/nutrition_data.db')

def simulate_data():
    bag = connect_db()
    b = bag.cursor()
    b.execute("SELECT name, category FROM foods")

    food_data = b.fetchall()
    food_names = [item[0] for item in food_data]
    
    weighted_foods = {
        'Meyve/Sebze': [f[0] for f in food_data if f[1] in ['Meyve', 'Sebze', 'Meze/Sos']],
        'Fast-Food/Tatlı': [f[0] for f in food_data if f[1] in ['Fast-Food', 'Tatlı', 'Atıştırmalık']],
        'Protein': [f[0] for f in food_data if f[1] in ['Protein Kaynağı', 'Deniz Ürünü', 'Kahvaltılık', 'Ana Yemek']]
    }


    print("100 Sanal Kullanıcı Oluşturuluyor...")
    for i in range(1, 101):
        gender = random.choice(['Erkek', 'Kadın'])
        age = random.randint(20, 60)
        weight = random.randint(55, 95)
        height = random.randint(160, 190)
        activity = random.choice(['Orta Hareketli', 'Az Hareketli', 'Hareketsiz'])
        goal = random.choice(['Kilo Ver', 'Kilo Koru', 'Kilo Al'])
        
        goal_calories = random.randint(1800, 3000)

        b.execute("INSERT OR REPLACE INTO users (id, name, gender, age, weight, height, activity_level, goal_type, goal_calories) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (i, f"User_{i}", gender, age, weight, height, activity, goal, goal_calories))

    

    print("5000+ Sanal Yemek Kaydi Olusturuluyor...")
    
    start_date = datetime.now() - timedelta(days=30)
    
    for user_id in range(1, 101):
        gender = 'Erkek' if user_id % 2 == 0 else 'Kadın'
        
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            
            
            meal_times = [8, 13, 19] 
            
            for hour in meal_times:
                meal_time = current_date.replace(hour=hour, minute=random.randint(0, 59))
                
               
                if gender == 'Kadın' and hour == 8:
                    food_choice = random.choices(weighted_foods['Meyve/Sebze'], k=1)[0] 
                elif hour >= 19:
                    food_choice = random.choices(weighted_foods['Fast-Food/Tatlı'], k=1)[0] 
                else:
                    food_choice = random.choice(food_names) 
                
                
                b.execute("INSERT INTO logs (user_id, food_name, timestamp) VALUES (?, ?, ?)",
                          (user_id, food_choice, meal_time))
    
    bag.commit()
    bag.close()
    print(" Buyuk veri simulesi tamamlandi.")

if __name__ == "__main__":
    simulate_data()