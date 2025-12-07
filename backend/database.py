import sqlite3
import pandas as pd
import random # Simülasyon için eklendi
from datetime import datetime, timedelta # Tarih ve simülasyon için eklendi

# --- TEMEL BAĞLANTI ---
def connect_db():
    return sqlite3.connect('backend/nutrition_data.db')

# --- HESAPLAMA MANTIĞI ---

def hesapla_gunluk_kalori(weight, height, age, gender, activity_level, goal_type):
    if gender == 'Erkek':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else: 
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    multipliers = {
        "Hareketsiz": 1.2,
        "Az Hareketli": 1.375,
        "Orta Hareketli": 1.55,
        "Çok Hareketli": 1.725,
        "Sporcu": 1.9
    }
    tdee = bmr * multipliers.get(activity_level, 1.55)

    # HATA OLAN KISIM BURADA TEMİZLENDİ.
    if goal_type == "Kilo Ver":
        target_calories = tdee - 500  
    elif goal_type == "Kilo Al":
        target_calories = tdee + 500  
    else:
        target_calories = tdee    
    return int(target_calories)

def create_database():

    bag = sqlite3.connect('backend/nutrition_data.db')
    b = bag.cursor()

    b.execute('''
        CREATE TABLE IF NOT EXISTS foods (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            calories INTEGER,
            protein REAL,
            carbs REAL,
            fat REAL,
            category TEXT
        )
    ''')

    b.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            age INTEGER,
            weight REAL,
            height REAL,
            activity_level TEXT, 
            goal_type TEXT,
            goal_calories INTEGER
        )
    ''')

    b.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            food_name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    food_list = [
        (0, 'Apple', 52, 0.3, 14.0, 0.2, 'Meyve'),
        (4, 'Banana', 89, 1.1, 22.8, 0.3, 'Meyve'),
        (12, 'Cantaloupe', 34, 0.8, 8.0, 0.2, 'Meyve'), 
        (15, 'Common-fig', 74, 0.8, 19.0, 0.3, 'Meyve'), 
        (25, 'Fruit', 50, 0.5, 13.0, 0.2, 'Meyve'), 
        (26, 'Grape', 69, 0.7, 18.0, 0.2, 'Meyve'),
        (32, 'Lemon', 29, 1.1, 9.0, 0.3, 'Meyve'), 
        (33, 'Mango', 60, 0.8, 15.0, 0.4, 'Meyve'),
        (36, 'Orange', 47, 0.9, 11.8, 0.1, 'Meyve'), 
        (41, 'Peach', 39, 0.9, 10.0, 0.3, 'Meyve'),
        (42, 'Pear', 57, 0.4, 15.0, 0.1, 'Meyve'), 
        (43, 'Pineapple', 50, 0.5, 13.0, 0.1, 'Meyve'),
        (45, 'Pomegranate', 83, 1.7, 19.0, 1.2, 'Meyve'), 
        (54, 'Strawberry', 32, 0.7, 7.7, 0.3, 'Meyve'),
        (62, 'Watermelon', 30, 0.6, 8.0, 0.2, 'Meyve'),
        (1, 'Asparagus', 20, 2.2, 3.9, 0.1, 'Sebze'), 
        (5, 'Bell-pepper', 20, 0.9, 4.6, 0.2, 'Sebze'),
        (7, 'Broccoli', 34, 2.8, 6.6, 0.4, 'Sebze'), 
        (9, 'Cabbage', 25, 1.3, 5.8, 0.1, 'Sebze'),
        (13, 'Carrot', 41, 0.9, 9.6, 0.2, 'Sebze'), 
        (18, 'Cucumber', 15, 0.7, 3.6, 0.1, 'Sebze'),
        (47, 'Potato', 77, 2.0, 17.0, 0.1, 'Sebze'), 
        (49, 'Salad', 33, 1.2, 4.0, 2.0, 'Sebze'),
        (59, 'Tomato', 18, 0.9, 3.9, 0.2, 'Sebze'), 
        (60, 'Vegetable', 25, 2.0, 5.0, 0.2, 'Sebze'),
        (8, 'Burrito', 206, 8.0, 25.0, 8.0, 'Fast-Food'), 
        (23, 'Fast-food', 295, 12.0, 30.0, 14.0, 'Fast-Food'),
        (24, 'French-fries', 312, 3.4, 41.0, 15.0, 'Fast-Food'), 
        (28, 'Hamburger', 295, 17.0, 30.0, 14.0, 'Fast-Food'),
        (30, 'Hot-dog', 290, 10.0, 25.0, 15.0, 'Fast-Food'), 
        (39, 'Pasta', 131, 5.0, 25.0, 1.1, 'Ana Yemek'),
        (44, 'Pizza', 266, 11.0, 33.0, 10.0, 'Fast-Food'), 
        (50, 'Sandwich', 250, 10.0, 35.0, 8.0, 'Ana Yemek'),
        (55, 'Submarine-sandwich', 250, 12.0, 30.0, 9.0, 'Ana Yemek'), 
        (56, 'Sushi', 179, 7.0, 35.0, 2.0, 'Deniz Ürünü'),
        (57, 'Taco', 226, 9.0, 20.0, 13.0, 'Fast-Food'), 
        (3, 'Baked-goods', 300, 5.0, 40.0, 15.0, 'Unlu Mamul'),
        (10, 'Cake', 257, 3.5, 45.0, 8.0, 'Tatlı'), 
        (11, 'Candy', 394, 0.0, 98.0, 0.2, 'Tatlı'),
        (16, 'Cookie', 502, 5.0, 65.0, 24.0, 'Tatlı'), 
        (20, 'Dessert', 300, 4.0, 50.0, 10.0, 'Tatlı'),
        (21, 'Doughnut', 452, 4.9, 51.0, 25.0, 'Tatlı'), 
        (29, 'Honeycomb', 300, 0.3, 82.0, 0.0, 'Tatlı'),
        (31, 'Ice-cream', 207, 3.5, 24.0, 11.0, 'Tatlı'), 
        (35, 'Muffin', 377, 4.5, 54.0, 16.0, 'Tatlı'),
        (38, 'Pancake', 227, 6.0, 28.0, 10.0, 'Tatlı'), 
        (40, 'Pastry', 350, 5.0, 45.0, 18.0, 'Tatlı'),
        (46, 'Popcorn', 375, 11.0, 74.0, 4.3, 'Atıştırmalık'), 
        (48, 'Pretzel', 380, 10.0, 80.0, 3.0, 'Atıştırmalık'),
        (53, 'Snack', 500, 5.0, 60.0, 25.0, 'Atıştırmalık'), 
        (58, 'Tart', 350, 3.0, 55.0, 15.0, 'Tatlı'),
        (61, 'Waffle', 291, 8.0, 33.0, 14.0, 'Tatlı'), 
        (2, 'Bagel', 250, 10.0, 49.0, 1.5, 'Unlu Mamul'),
        (6, 'Bread', 265, 9.0, 49.0, 3.2, 'Unlu Mamul'), 
        (14, 'Cheese', 402, 25.0, 1.3, 33.0, 'Kahvaltılık'),
        (17, 'Croissant', 406, 8.0, 46.0, 21.0, 'Unlu Mamul'), 
        (19, 'Dairy', 60, 3.0, 5.0, 3.0, 'Kahvaltılık'),
        (22, 'Egg', 155, 13.0, 1.1, 11.0, 'Kahvaltılık'), 
        (27, 'Guacamole', 160, 2.0, 9.0, 15.0, 'Meze/Sos'),
        (34, 'Milk', 42, 3.4, 5.0, 1.0, 'Kahvaltılık'), 
        (37, 'Oyster', 81, 9.0, 5.0, 2.0, 'Deniz Ürünü'),
        (51, 'Seafood', 100, 20.0, 1.0, 2.0, 'Deniz Ürünü'), 
        (52, 'Shrimp', 99, 24.0, 0.2, 0.3, 'Deniz Ürünü')
    ]

    b.executemany('INSERT OR REPLACE INTO foods (id, name, calories, protein, carbs, fat, category) VALUES (?, ?, ?, ?, ?, ?, ?)', food_list)

    demo_user = {
        "name": "Demo BERKAY", "gender": "Erkek", "age": 21, "weight": 60, "height": 170,
        "activity": "Orta Hareketli", "goal": "Kilo Al"
    }

    final_goal_calories = hesapla_gunluk_kalori(
        demo_user["weight"], demo_user["height"], demo_user["age"], demo_user["gender"], demo_user["activity"], demo_user["goal"]
    )
    
    print(f"Kullanici: {demo_user['name']} / Hedef: {final_goal_calories} kcal")

    b.execute('''
        INSERT OR IGNORE INTO users (name, gender, age, weight, height, activity_level, goal_type, goal_calories)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (demo_user["name"], demo_user["gender"], demo_user["age"], demo_user["weight"], demo_user["height"], demo_user["activity"], demo_user["goal"], final_goal_calories))
    
    bag.commit()
    bag.close()
    print("Veritabani güncellendi nutrition_data.db olustu.")
    print(f"Veritabani hazir toplam {len(food_list)} besin.")

def save_user_profile(user_id, name, gender, age, weight, height, activity, goal, calories):
    
    bag = sqlite3.connect('backend/nutrition_data.db')
    b = bag.cursor()

    # Kullanıcıyı güncelleme sorgusu (9 argüman alır)
    b.execute('''
        INSERT OR REPLACE INTO users (id, name, gender, age, weight, height, activity_level, goal_type, goal_calories)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, name, gender, age, weight, height, activity, goal, calories))
    
    bag.commit()
    bag.close()

def get_demo_user_id():
    """Demo kullanıcı ID'sini çeker."""
    bag = sqlite3.connect('backend/nutrition_data.db')
    b = bag.cursor()
    b.execute("SELECT id FROM users WHERE name='Demo BERKAY' OR name='Demo Öğrenci' LIMIT 1")
    user_id = b.fetchone()
    bag.close()
    return user_id[0] if user_id else 1 # ID yoksa 1 döndür

def save_log(user_id, food_name):
    """Analiz edilen yemeği ZAMAN DAMGASI ile Log tablosuna kaydeder."""
    bag = connect_db() 
    b = bag.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Zaman damgası
    
    # Logs tablosuna kaydetmek
    b.execute("INSERT INTO logs (user_id, food_name, timestamp) VALUES (?, ?, ?)", 
              (user_id, food_name, current_time))
    
    bag.commit()
    bag.close()

def get_all_users_profiles():
    """Tüm kullanıcı ID'lerini ve isimlerini çeker."""
    bag = connect_db()
    # Tüm sütunları çekiyoruz çünkü app.py bu verilere ihtiyaç duyuyor.
    users_df = pd.read_sql_query("SELECT * FROM users", bag)
    bag.close()
    return users_df

# --- SİMÜLASYON FONKSİYONLARI ---

def generate_7_day_logs_for_100_users(start_user_id=1, end_user_id=100):
    """
    100 farklı kullanıcı için 7 günlük rastgele log kaydı oluşturur.
    """
    bag = sqlite3.connect('backend/nutrition_data.db')
    b = bag.cursor()

    food_names_result = b.execute("SELECT name, category FROM foods").fetchall()
    if not food_names_result:
        print("HATA: Foods tablosu boş. Simülasyon verisi üretilemiyor.")
        bag.close()
        return

    food_data = b.fetchall() # foods tablosundaki veriyi çekelim
    food_names = [item[0] for item in food_names_result] # Sadece isimler
    
    # Simülasyon Veri Seti için Kategori Ağırlıkları
    weighted_foods = {
        'Meyve/Sebze': [f[0] for f in food_names_result if f[1] in ['Meyve', 'Sebze', 'Meze/Sos']],
        'Fast-Food/Tatlı': [f[0] for f in food_names_result if f[1] in ['Fast-Food', 'Tatlı', 'Atıştırmalık']],
        'Protein': [f[0] for f in food_names_result if f[1] in ['Protein Kaynağı', 'Deniz Ürünü', 'Kahvaltılık', 'Ana Yemek']]
    }
    
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Eski simülasyon loglarını silelim
    b.execute(f"DELETE FROM logs WHERE user_id BETWEEN {start_user_id} AND {end_user_id}")
    
    # 2. 100 Kullanıcı Döngüsü
    for user_id in range(start_user_id, end_user_id + 1):
        
        # Kullanıcı profili oluştur/güncelle (eğer yoksa)
        if user_id > 1: # Demo Berkay ID 1'de kalabilir
            random_age = random.randint(18, 60)
            random_weight = random.uniform(50.0, 100.0)
            random_height = random.randint(160, 190)
            random_gender = random.choice(['Erkek', 'Kadın'])
            random_activity = random.choice(["Az Hareketli", "Orta Hareketli", "Çok Hareketli"])
            random_goal = random.choice(["Kilo Koru", "Kilo Ver", "Kilo Al"])
            
            calculated_goal = hesapla_gunluk_kalori(random_weight, random_height, random_age, random_gender, random_activity, random_goal)
            
            b.execute('''
                INSERT OR REPLACE INTO users (id, name, gender, age, weight, height, activity_level, goal_type, goal_calories)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, f'SimUser_{user_id}', random_gender, random_age, random_weight, random_height, random_activity, random_goal, calculated_goal))

        # 3. 7 Günlük Log Döngüsü
        for day_offset in range(1, 8):
            log_date = today - timedelta(days=day_offset)
            
            meal_times = [8, 13, 19] 
            
            for hour in meal_times:
                meal_time = log_date.replace(hour=hour, minute=random.randint(0, 59))
                
                gender = 'Erkek' if user_id % 2 == 0 else 'Kadın'
                
                # Kadınlar sabahları meyve/sebzeye, Akşamları Tatlıya daha eğilimli olsun (Analizden anlamlı sonuç çıkması için)
                if gender == 'Kadın' and hour == 8:
                    food_choice = random.choices(weighted_foods['Meyve/Sebze'], k=1)[0]
                elif hour >= 19:
                    food_choice = random.choices(weighted_foods['Fast-Food/Tatlı'], k=1)[0]
                else:
                    food_choice = random.choice(food_names)
                
                # Log kaydı (timestamp ile)
                b.execute("INSERT INTO logs (user_id, food_name, timestamp) VALUES (?, ?, ?)", 
                          (user_id, food_choice, meal_time.strftime("%Y-%m-%d %H:%M:%S")))

    bag.commit()
    bag.close()
    print(f"✅ Başarılı! {end_user_id - start_user_id + 1} kullanıcı için 7 günlük simülasyon kaydı oluşturuldu.")


if __name__ == "__main__":
    create_database()
    generate_7_day_logs_for_100_users(start_user_id=1, end_user_id=100)