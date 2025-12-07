# 📊 Gerçek Veri Giriş Formatı

## 🎯 İHTİYAÇ

100 kişinin 7 günlük gerçek yemek verilerini sisteme girmek istiyorsunuz.

---

## 📝 VERİ FORMATI (Excel/CSV)

### Dosya 1: `kullanicilar.csv`

```csv
ad_soyad,cinsiyet,yas,kilo,boy,aktivite,hedef
Ahmet Yılmaz,Erkek,25,75,175,Orta Hareketli,Kilo Ver
Ayşe Demir,Kadın,28,60,165,Az Hareketli,Kilo Koru
Mehmet Kaya,Erkek,35,85,180,Çok Hareketli,Kilo Al
Fatma Şahin,Kadın,22,55,160,Hareketsiz,Kilo Ver
... (100 kişi)
```

**Sütunlar:**
- `ad_soyad`: Kişinin adı
- `cinsiyet`: Erkek veya Kadın
- `yas`: 18-80 arası
- `kilo`: kg cinsinden
- `boy`: cm cinsinden
- `aktivite`: Hareketsiz, Az Hareketli, Orta Hareketli, Çok Hareketli, Sporcu
- `hedef`: Kilo Ver, Kilo Koru, Kilo Al

---

### Dosya 2: `yemek_kayitlari.csv`

```csv
ad_soyad,tarih,saat,yemek_adi
Ahmet Yılmaz,2025-01-01,08:30,Egg
Ahmet Yılmaz,2025-01-01,08:35,Bread
Ahmet Yılmaz,2025-01-01,13:00,Chicken
Ahmet Yılmaz,2025-01-01,13:05,Salad
Ahmet Yılmaz,2025-01-01,19:30,Fish
Ahmet Yılmaz,2025-01-02,08:00,Cheese
... (7 gün × 3-5 öğün × 100 kişi = ~3000 kayıt)
```

**Sütunlar:**
- `ad_soyad`: Hangi kullanıcı (kullanicilar.csv'deki ile eşleşmeli)
- `tarih`: YYYY-MM-DD formatında (örn: 2025-01-01)
- `saat`: HH:MM formatında (örn: 08:30)
- `yemek_adi`: Veritabanındaki yemek adı (Apple, Pizza, Salad vs.)

---

## 🍽️ KULLANILABILIR YEMEK ADLARI

Veritabanında 63 yemek var. İşte tam liste:

### Meyveler:
Apple, Banana, Cantaloupe, Common-fig, Fruit, Grape, Lemon, Mango, Orange, Peach, Pear, Pineapple, Pomegranate, Strawberry, Watermelon

### Sebzeler:
Asparagus, Bell-pepper, Broccoli, Cabbage, Carrot, Cucumber, Potato, Salad, Tomato, Vegetable

### Fast-Food:
Burrito, Fast-food, French-fries, Hamburger, Hot-dog, Pizza, Taco

### Ana Yemek:
Pasta, Sandwich, Submarine-sandwich, Sushi

### Tatlı:
Baked-goods, Cake, Candy, Cookie, Dessert, Doughnut, Honeycomb, Ice-cream, Muffin, Pancake, Pastry, Tart, Waffle

### Atıştırmalık:
Popcorn, Pretzel, Snack

### Kahvaltılık/Protein:
Bagel, Bread, Cheese, Croissant, Dairy, Egg, Milk

### Deniz Ürünü:
Oyster, Seafood, Shrimp

### Diğer:
Guacamole

---

## 📤 ÖRNEK VERİ DOSYALARI

### `kullanicilar.csv` (Örnek 10 kişi)

```csv
ad_soyad,cinsiyet,yas,kilo,boy,aktivite,hedef
Ahmet Yılmaz,Erkek,25,75,175,Orta Hareketli,Kilo Ver
Ayşe Demir,Kadın,28,60,165,Az Hareketli,Kilo Koru
Mehmet Kaya,Erkek,35,85,180,Çok Hareketli,Kilo Al
Fatma Şahin,Kadın,22,55,160,Hareketsiz,Kilo Ver
Can Öztürk,Erkek,30,80,178,Orta Hareketli,Kilo Koru
Zeynep Aydın,Kadın,26,65,168,Az Hareketli,Kilo Ver
Ali Çelik,Erkek,40,90,182,Çok Hareketli,Kilo Al
Elif Arslan,Kadın,24,58,162,Orta Hareketli,Kilo Koru
Burak Yıldız,Erkek,32,78,176,Az Hareketli,Kilo Ver
Seda Kara,Kadın,29,62,166,Orta Hareketli,Kilo Al
```

---

### `yemek_kayitlari.csv` (Örnek 1 gün - Ahmet Yılmaz)

```csv
ad_soyad,tarih,saat,yemek_adi
Ahmet Yılmaz,2025-01-01,08:00,Egg
Ahmet Yılmaz,2025-01-01,08:05,Bread
Ahmet Yılmaz,2025-01-01,08:10,Cheese
Ahmet Yılmaz,2025-01-01,13:00,Chicken
Ahmet Yılmaz,2025-01-01,13:05,Salad
Ahmet Yılmaz,2025-01-01,13:10,Tomato
Ahmet Yılmaz,2025-01-01,19:30,Fish
Ahmet Yılmaz,2025-01-01,19:35,Broccoli
Ahmet Yılmaz,2025-01-01,19:40,Potato
```

**Not:** Bunu 7 gün × 100 kişi için tekrarlayın!

---

## 🚀 VERİYİ SİSTEME AKTARMA

### Yöntem 1: Python Script (Otomatik)

Veriyi hazırladıktan sonra şu scripti kullanın:

```python
import pandas as pd
from backend.database import save_user_profile, save_log, hesapla_gunluk_kalori

# 1. Kullanıcıları ekle
users_df = pd.read_csv('kullanicilar.csv')

for idx, row in users_df.iterrows():
    user_id = idx + 1  # ID'ler 1'den başlar
    
    hedef_kalori = hesapla_gunluk_kalori(
        row['kilo'], row['boy'], row['yas'], 
        row['cinsiyet'], row['aktivite'], row['hedef']
    )
    
    save_user_profile(
        user_id, row['ad_soyad'], row['cinsiyet'], row['yas'],
        row['kilo'], row['boy'], row['aktivite'], row['hedef'], hedef_kalori
    )
    print(f"✅ {row['ad_soyad']} eklendi (ID: {user_id})")

# 2. Yemek kayıtlarını ekle
logs_df = pd.read_csv('yemek_kayitlari.csv')
user_name_to_id = dict(zip(users_df['ad_soyad'], range(1, len(users_df)+1)))

for idx, row in logs_df.iterrows():
    user_id = user_name_to_id[row['ad_soyad']]
    timestamp = f"{row['tarih']} {row['saat']}:00"
    
    save_log(user_id, row['yemek_adi'], timestamp)
    
    if idx % 100 == 0:
        print(f"📝 {idx} kayıt eklendi...")

print(f"🎉 Toplam {len(logs_df)} kayıt eklendi!")
```

**Kullanım:**
```bash
python import_real_data.py
```

---

### Yöntem 2: Manuel (Uygulamada)

1. Uygulamayı açın
2. Sol panelde "➕ Yeni Kullanıcı Ekle"
3. Her kişiyi manuel ekleyin
4. Yemek fotoğraflarını yükleyin + tarih/saat seçin
5. "Analiz ve Kaydet" butonuna basın

**Uyarı:** 100 kişi × 7 gün manuel giriş çok uzun sürer!

---

## 🧹 SİMÜLE VERİYİ TEMİZLEME

Gerçek veri eklemeden önce simüle veriyi temizleyin:

```python
import sqlite3

conn = sqlite3.connect('backend/nutrition_data.db')
cursor = conn.cursor()

# Tüm logları sil
cursor.execute("DELETE FROM logs")

# Demo BERKAY hariç tüm kullanıcıları sil
cursor.execute("DELETE FROM users WHERE id > 1")

conn.commit()
conn.close()

print("✅ Simüle veriler temizlendi!")
```

---

## 📊 ÖNERİLEN İŞ AKIŞI

### Adım 1: Veri Toplama
- Excel dosyası hazırlayın
- 100 kişinin bilgilerini girin
- 7 günlük yemek kayıtlarını girin

### Adım 2: Veriyi Kontrol Etme
- Yemek adları doğru mu? (Apple, Pizza vs.)
- Tarih formatı doğru mu? (YYYY-MM-DD)
- Saat formatı doğru mu? (HH:MM)

### Adım 3: Import Scripti Çalıştırma
```bash
python import_real_data.py
```

### Adım 4: Kontrol
```bash
streamlit run app.py
# "Genel Korelasyon Analizi" butonuna bas
# Gerçek verileri gör!
```

---

## 💡 İPUÇLARI

1. **Yemek Adları:** Veritabanındaki adlarla birebir eşleşmeli (büyük/küçük harf önemli)
2. **Tarih Formatı:** Mutlaka YYYY-MM-DD (örn: 2025-01-15)
3. **Saat Formatı:** HH:MM (örn: 08:30, 19:00)
4. **7 Günlük:** Her kişi için tam 7 gün veri olsun
5. **Tutarlılık:** Aynı kişi için tutarlı yemek saatleri (kahvaltı ~08:00, öğle ~13:00, akşam ~19:00)

---

## ❓ SSS

**S: 100 kişinin 7 günlük verisini nasıl toplayacağım?**
C: Arkadaşlarınızdan, ailenizden, anket yaparak. Veya varsayımsal ama gerçekçi veriler oluşturabilirsiniz.

**S: Her yemek için fotoğraf mı gerekli?**
C: Hayır! CSV ile direkt veritabanına ekleyebilirsiniz.

**S: Simüle veri kalmalı mı?**
C: Hayır, temizleyin. Gerçek veri daha değerli.

**S: 100 kişi çok fazla, 20-30 kişi olabilir mi?**
C: Evet! Önemli olan gerçek veri olması, sayı esnektir.

---

## 🎉 SONUÇ

Gerçek veri ile:
- ✅ Daha anlamlı korelasyonlar
- ✅ Hocaya daha inandırıcı sunum
- ✅ Gerçek besin tercihleri analizi
- ✅ Akademik olarak daha değerli

**Verilerinizi hazırladıktan sonra bana gönderin, import scriptini ben yazarım!** 📤
