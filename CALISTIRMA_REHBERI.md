# 🚀 Projeyi Çalıştırma Rehberi

## 📋 İÇİNDEKİLER
1. [Gereksinimler](#gereksinimler)
2. [Adım Adım Kurulum](#adım-adım-kurulum)
3. [Uygulamayı Çalıştırma](#uygulamayı-çalıştırma)
4. [Sorun Giderme](#sorun-giderme)

---

## 🎯 GEREKSİNİMLER

### Bilgisayarınızda olması gerekenler:
- ✅ **Python 3.8 veya üzeri** (Python 3.11 önerilir)
- ✅ **Git** (GitHub'dan indirmek için)
- ✅ **İnternet bağlantısı** (kütüphaneleri indirmek için)

### Python Kurulu mu Kontrol Edin:
**Windows:**
```cmd
python --version
```

**Mac/Linux:**
```bash
python3 --version
```

Eğer "command not found" hatası alırsanız → Python kurmanız gerekiyor:
- **Windows:** https://www.python.org/downloads/ (İndirirken "Add to PATH" seçeneğini işaretleyin!)
- **Mac:** `brew install python` veya python.org'dan indirin
- **Linux:** `sudo apt install python3 python3-pip`

---

## 📥 ADIM ADIM KURULUM

### ADIM 1: Projeyi İndirin

Terminal veya Komut İstemi'ni açın, sonra:

```bash
# Projeyi GitHub'dan klonlayın
git clone https://github.com/aberk4y/gorselbeslenme_proje.git

# Proje klasörüne girin
cd gorselbeslenme_proje
```

**Not:** Git yüklü değilse, GitHub sayfasından ZIP olarak indirip çıkartın:
1. https://github.com/aberk4y/gorselbeslenme_proje
2. Yeşil "Code" butonu → "Download ZIP"
3. ZIP'i çıkartın ve Terminal'de o klasöre gidin

---

### ADIM 2: Python Kütüphanelerini Kurun

Proje klasöründeyken:

**Windows:**
```cmd
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
pip3 install -r requirements.txt
```

**Bu işlem birkaç dakika sürebilir!** Şunlar yüklenecek:
- Streamlit (Web arayüzü)
- YOLOv8 (Yapay zeka modeli)
- OpenCV (Görüntü işleme)
- Pandas (Veri analizi)
- ve diğerleri...

---

### ADIM 3: Veritabanını Oluşturun

```bash
# Windows
python -m backend.database

# Mac/Linux
python3 -m backend.database
```

**Ne yapılıyor?**
- SQLite veritabanı oluşturuluyor
- 63 besin kaydı ekleniyor
- Demo kullanıcı oluşturuluyor
- 100 kullanıcı için simülasyon verisi üretiliyor

**Göreceğiniz Çıktı:**
```
Kullanici: Demo BERKAY / Hedef: 2921 kcal
Veritabani güncellendi nutrition_data.db olustu.
Veritabani hazir toplam 63 besin.
✅ Başarılı! 100 kullanıcı için 7 günlük simülasyon kaydı oluşturuldu.
```

---

## 🎮 UYGULAMAYI ÇALIŞTIRMA

### Uygulamayı Başlatın:

**Windows:**
```cmd
streamlit run app.py
```

**Mac/Linux:**
```bash
streamlit run app.py
```

**Ne olacak?**
1. Terminal'de şöyle bir mesaj göreceksiniz:
   ```
   You can now view your Streamlit app in your browser.

   Local URL: http://localhost:8501
   Network URL: http://192.168.1.x:8501
   ```

2. Tarayıcınız **otomatik olarak açılacak**

3. Açılmazsa → `http://localhost:8501` adresine manuel gidin

---

## 🎨 UYGULAMAYI KULLANMA

### İlk Kullanım:

1. **Sol Panelden Kullanıcı Seçin**
   - "Demo BERKAY" veya başka bir kullanıcı seçin

2. **Tarih ve Saat Ayarlayın**
   - Bugünün tarihi otomatik gelir
   - İsterseniz değiştirebilirsiniz

3. **Yemek Fotoğrafı Yükleyin**
   - "Browse files" butonuna tıklayın
   - Pizza, salata, meyve vs. fotoğrafı seçin

4. **Analiz Yapın**
   - "Analiz Yap ve KAYDET" butonuna basın
   - Yapay zeka yemeği tanıyacak
   - Kalori ve besin değerleri gösterilecek

5. **Rapor Görüntüleyin**
   - Sağ sütunda tarih aralığı seçin
   - "Seçili Kullanıcının Takip Raporu" butonuna basın
   - Grafikler ve analizler görünecek

---

## ⚠️ SORUN GİDERME

### Sorun 1: "python command not found"
**Çözüm:**
- Python kurulu değil → Python'u kurun
- Veya `python3` deneyin (Mac/Linux'ta)

---

### Sorun 2: "No module named 'streamlit'"
**Çözüm:**
```bash
pip install streamlit
# veya
pip install -r requirements.txt
```

---

### Sorun 3: "ModuleNotFoundError: No module named 'ultralytics'"
**Çözüm:**
```bash
pip install ultralytics
```

---

### Sorun 4: "Address already in use" (Port 8501 kullanımda)
**Çözüm:**
```bash
# Farklı port kullanın
streamlit run app.py --server.port=8502
```

---

### Sorun 5: Model Yükleme Uyarısı (PyTorch 2.6+)
**Durum:** "Weights only load failed" uyarısı
**Çözüm:** Bu uyarı normal, işlevselliği etkilemiyor. Görmezden gelebilirsiniz.

Düzeltmek isterseniz:
```bash
pip install torch==2.0.0 torchvision==0.15.0
```

---

### Sorun 6: Veritabanı Hatası
**Çözüm:**
```bash
# Veritabanını yeniden oluşturun
python -m backend.database
```

---

### Sorun 7: Fotoğraf Analiz Edilmiyor
**Olası Nedenler:**
1. Model dosyası (`backend/best.pt`) eksik
2. Fotoğraf formatı desteklenmiyor (JPG, PNG, JPEG kullanın)
3. İnternet bağlantısı yok (ilk çalıştırmada gerekli)

**Çözüm:**
- `backend/best.pt` dosyasının 6MB civarında olduğunu kontrol edin
- Farklı bir fotoğraf deneyin

---

## 🔄 UYGULAMAYI DURDURMA

**Terminal'de:**
- Windows/Mac/Linux: `Ctrl + C` tuşlarına basın

**Tarayıcı:**
- Sekmeyi kapatabilirsiniz (uygulama arka planda çalışmaya devam eder)

---

## 🎓 İPUÇLARI

### ✅ İyi Sonuç İçin:
1. **Net Fotoğraflar Kullanın:** Bulanık fotoğraflar hata verebilir
2. **Tek Yemek:** Her fotoğrafta bir yemek olsun
3. **İyi Işıklandırma:** Karanlık fotoğraflar tanınmayabilir
4. **Desteklenen Yemekler:** 63 çeşit yemek tanınabilir (elma, muz, pizza, salata vb.)

### ✅ Test İçin:
- Google'dan "pizza photo" arayın
- İndirin ve uygulamaya yükleyin
- Sistem pizzayı tanıyıp kalori hesaplayacak

---

## 📊 KLASİK KULLANIM SENARYOSU

```
1. Sabah 08:00 - Kahvaltı
   - Tarih: Bugün, Saat: 08:00
   - Fotoğraf: Yumurta + Ekmek
   - KAYDET

2. Öğle 13:00 - Öğle Yemeği
   - Tarih: Bugün, Saat: 13:00
   - Fotoğraf: Tavuk + Pilav
   - KAYDET

3. Akşam 19:30 - Akşam Yemeği
   - Tarih: Bugün, Saat: 19:30
   - Fotoğraf: Salata
   - KAYDET

4. Rapor Görüntüle
   - Başlangıç: Bugün
   - Bitiş: Bugün
   - "Takip Raporu" butonuna bas
   - ✅ Günün grafiği görünür!
```

---

## 🎉 BAŞARIYLA ÇALIŞIRSA

Şunları göreceksiniz:
- ✅ Streamlit arayüzü açılır
- ✅ Kullanıcı profilleri görünür
- ✅ Fotoğraf yüklenebilir
- ✅ Yapay zeka yemekleri tanır
- ✅ Grafikler oluşturulur

---

## 📞 YARDIM

Hala sorun mu yaşıyorsunuz?

1. **Hata Mesajını Kopyalayın:** Terminal'deki hata mesajının ekran görüntüsünü alın
2. **Hangi Adımda Takıldınız:** Sorunun hangi adımda olduğunu belirtin
3. **Python Versiyonunuz:** `python --version` çıktısını paylaşın

---

## ✅ KONTROL LİSTESİ

Çalıştırma öncesi kontrol edin:

- [ ] Python kurulu (3.8+)
- [ ] Git kurulu (veya ZIP indirildi)
- [ ] Proje klasörü indirildi
- [ ] `requirements.txt` kuruldu
- [ ] Veritabanı oluşturuldu (`python -m backend.database`)
- [ ] `streamlit run app.py` komutu çalıştırıldı
- [ ] Tarayıcıda `localhost:8501` açıldı

Hepsi ✅ ise → **Başarılı!** Uygulamanız çalışıyor! 🎉

---

## 🚀 HIZLI BAŞLANGIÇ (Özet)

```bash
# 1. İndirin
git clone https://github.com/aberk4y/gorselbeslenme_proje.git
cd gorselbeslenme_proje

# 2. Kütüphaneleri kurun
pip install -r requirements.txt

# 3. Veritabanını oluşturun
python -m backend.database

# 4. Çalıştırın
streamlit run app.py

# 5. Tarayıcıda açın
# http://localhost:8501
```

**İşte bu kadar! Keyifli kullanımlar!** 🍽️
