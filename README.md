# 🍽️ Görsel Besin Analiz Sistemi

YOLOv8 tabanlı yapay zeka destekli besin analiz ve kalori takip uygulaması.

## 📋 Özellikler

- **YOLOv8 Nesne Tespiti**: Yemek fotoğraflarından otomatik besin tanıma
- **Kalori Hesaplama**: BMR/TDEE bazlı kişiselleştirilmiş kalori hedefleri
- **Besin Takibi**: Protein, karbonhidrat ve yağ takibi
- **Haftalık Raporlar**: Kullanıcıya özel tüketim analizleri
- **Korelasyon Analizi**: 5000+ kayıt üzerinden genel trendler
- **Çoklu Kullanıcı Desteği**: Birden fazla kullanıcı profili yönetimi

## 🚀 Kurulum

### Gereksinimler
- Python 3.11+
- CUDA destekli GPU (isteğe bağlı, hızlandırma için)

### Bağımlılıklar
```bash
pip install -r requirements.txt
```

### Veritabanı Kurulumu
```bash
python -m backend.database
```

Bu komut:
- SQLite veritabanını oluşturur
- 63 besin kaydını ekler
- Demo kullanıcı oluşturur
- 100 kullanıcı için 7 günlük simülasyon verisi üretir

## 🎯 Kullanım

### Uygulamayı Başlatma
```bash
streamlit run app.py
```

### Temel İşlevler

1. **Profil Yönetimi** (Sol Panel)
   - Kullanıcı seçimi
   - Profil güncelleme (yaş, kilo, boy, aktivite seviyesi)
   - Hedef belirleme (kilo ver, koru, al)

2. **Yemek Analizi** (Sol Sütun)
   - Fotoğraf yükleme
   - Yapay zeka ile otomatik tespit
   - Kalori ve besin değerlerinin hesaplanması
   - Otomatik kayıt

3. **Raporlar** (Sağ Sütun)
   - Haftalık tüketim grafikleri
   - Makro besin dağılımı
   - Genel korelasyon analizleri

## 📁 Proje Yapısı

```
gorselbeslenme_proje/
├── app.py                      # Ana Streamlit uygulaması
├── backend/
│   ├── analiz.py              # YOLOv8 görüntü analizi
│   ├── database.py            # Veritabanı işlemleri
│   ├── yolotanim.py           # Model yükleme
│   ├── yolotrain.py           # Model eğitimi (opsiyonel)
│   ├── ddata.py               # Roboflow veri indirme
│   ├── sistem_sim.py          # Eski simülasyon scripti
│   ├── best.pt                # Eğitilmiş YOLOv8 modeli
│   └── nutrition_data.db      # SQLite veritabanı
├── requirements.txt           # Python bağımlılıkları
└── README.md                  # Bu dosya
```

## 🔧 Düzeltilen Hatalar

### v1.1 Güncellemeleri
1. ✅ **Import Hataları**: `backend/analiz.py` dosyasındaki çift import düzeltildi
2. ✅ **Kategori Tutarsızlığı**: 'Baked-goods' kategorisi 'Unlu Mamul' olarak güncellendi
3. ✅ **Hata Yakalama**: `app.py` içinde daha iyi hata mesajları eklendi
4. ✅ **Gereksiz Dosyalar**: `dt.py` ve `fff.py` dosyaları temizlendi
5. ✅ **PyTorch 2.6+ Uyumluluk**: Model yükleme uyarıları iyileştirildi

## ⚠️ Bilinen Sorunlar

### Model Yükleme
- **Sorun**: PyTorch 2.6+ ile model yükleme hatası
- **Neden**: Eski PyTorch sürümü ile eğitilmiş model dosyası
- **Geçici Çözüm**: Uyarılar göz ardı edilebilir
- **Kalıcı Çözüm**: 
  ```bash
  # Model yeniden eğitimi için
  python backend/yolotrain.py
  ```

## 🧪 Test

### Veritabanı Testi
```bash
python -m backend.database
```

### Model Testi
```bash
python backend/yolotanim.py
```

### Analiz Testi
```bash
python backend/analiz.py
```

## 📊 Veritabanı Şeması

### foods
- `id`: Benzersiz besin ID
- `name`: Besin adı
- `calories`: 100g başına kalori
- `protein`: 100g başına protein (g)
- `carbs`: 100g başına karbonhidrat (g)
- `fat`: 100g başına yağ (g)
- `category`: Kategori (Meyve, Sebze, Fast-Food, vb.)

### users
- `id`: Kullanıcı ID
- `name`: Ad Soyad
- `gender`: Cinsiyet
- `age`: Yaş
- `weight`: Kilo (kg)
- `height`: Boy (cm)
- `activity_level`: Aktivite seviyesi
- `goal_type`: Hedef (Kilo Ver/Koru/Al)
- `goal_calories`: Hedef kalori

### logs
- `id`: Kayıt ID
- `user_id`: Kullanıcı referansı
- `food_name`: Tüketilen besin
- `timestamp`: Zaman damgası

## 🎓 Eğitim Verisi

Model, Roboflow üzerinden indirilen 63 sınıflı yemek veri seti ile eğitilmiştir.

### Veri İndirme
```bash
python backend/ddata.py
```

## 📝 Lisans

Bu proje akademik amaçlı geliştirilmiştir.

## 👨‍💻 Geliştirici

- **Proje Adı**: Görsel Besin Analiz Sistemi
- **Demo Kullanıcı**: Demo BERKAY
- **Teknolojiler**: Python, Streamlit, YOLOv8, SQLite, Pandas

## 🔄 Güncellemeler

### v1.1 (Son Güncelleme)
- Import hatalarının düzeltilmesi
- Kategori tutarlılığının sağlanması
- Hata mesajlarının iyileştirilmesi
- PyTorch uyumluluk güncellemeleri
- Kod temizliği ve dokümantasyon

## 💡 İpuçları

1. **İlk Kullanım**: Veritabanını mutlaka oluşturun (`python -m backend.database`)
2. **Model Sorunu**: Eğer model yüklenmiyorsa, YOLOv8n.pt ile yeniden eğitim yapın
3. **Simülasyon**: Hızlı test için simülasyon verisi kullanın
4. **Gerçek Veri**: Kendi yemek fotoğraflarınızı yükleyerek test edin

## 📞 Destek

Sorularınız için proje deposuna issue açabilirsiniz.
