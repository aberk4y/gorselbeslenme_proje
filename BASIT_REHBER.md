# 🎯 Basit Çalıştırma Rehberi (5 Adım)

## Bilgisayarınızda çalıştırmak için:

---

## 📥 ADIM 1: Projeyi İndirin

### Seçenek A: Git ile (Önerilir)
Terminal veya Komut İstemi açın:
```bash
git clone https://github.com/aberk4y/gorselbeslenme_proje.git
cd gorselbeslenme_proje
```

### Seçenek B: ZIP ile
1. https://github.com/aberk4y/gorselbeslenme_proje adresine gidin
2. Yeşil "Code" butonuna tıklayın
3. "Download ZIP" seçin
4. ZIP'i çıkartın
5. Terminal'de o klasöre gidin:
   ```bash
   cd C:\Users\YourName\Downloads\gorselbeslenme_proje
   ```

---

## 🔧 ADIM 2: Kütüphaneleri Kurun

```bash
pip install -r requirements.txt
```

**Bekleme süresi:** 2-5 dakika

---

## 🗄️ ADIM 3: Veritabanını Hazırlayın

```bash
python -m backend.database
```

**Göreceğiniz:**
```
✅ Başarılı! 100 kullanıcı için 7 günlük simülasyon kaydı oluşturuldu.
```

---

## 🚀 ADIM 4: Uygulamayı Başlatın

```bash
streamlit run app.py
```

**Tarayıcınız otomatik açılacak!**

Açılmazsa → http://localhost:8501

---

## 🎮 ADIM 5: Kullanmaya Başlayın!

1. **Sol panelden kullanıcı seçin** (örn: Demo BERKAY)
2. **Tarih ve saat ayarlayın**
3. **Yemek fotoğrafı yükleyin**
4. **"Analiz Yap ve KAYDET" butonuna basın**
5. **Sağ taraftan rapor görüntüleyin**

---

## ❌ Hata Alırsanız?

### "python command not found"
**Çözüm:** Python kurun → https://www.python.org/downloads/

### "No module named 'streamlit'"
**Çözüm:** 
```bash
pip install -r requirements.txt
```

### "Port already in use"
**Çözüm:** 
```bash
streamlit run app.py --server.port=8502
```

---

## 💡 HIZLI TEST

Uygulamayı test etmek için:

1. Google'dan "salad photo" arayın ve bir resim indirin
2. Uygulamada resmi yükleyin
3. "Analiz Yap" butonuna basın
4. ✅ Sistem salatayı tanıyıp kalori hesaplamalı!

---

## 🎉 BAŞARILI!

Eğer tarayıcınızda uygulama göründüyse → **Tebrikler!** Projeniz çalışıyor! 🎊

---

## 🛑 Durdurmak İçin

Terminal'de: **Ctrl + C**

---

## 📞 Sorun mu var?

Detaylı rehber için: **CALISTIRMA_REHBERI.md** dosyasını okuyun
