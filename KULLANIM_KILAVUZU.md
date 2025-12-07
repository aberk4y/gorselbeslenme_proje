# 📖 Kullanım Kılavuzu - Görsel Besin Analiz Sistemi

## 🎉 YENİ ÖZELLİKLER (v2.0)

### ✅ 1. MANUEL TARİH VE SAAT GİRİŞİ
Artık yemek kaydı yaparken **istediğiniz tarih ve saati** seçebilirsiniz!

**Nasıl Kullanılır:**
1. Fotoğraf yükleyin
2. **"Tarih Seçin"** alanından istediğiniz günü seçin
3. **"Saat Seçin"** alanından saati belirleyin
4. "Analiz Yap ve KAYDET" butonuna basın

**Örnek Kullanım:**
- Dün akşam yediğiniz yemeği bugün ekleyebilirsiniz
- Geçmiş tarihlere veri girebilirsiniz
- Her yemek için ayrı saat seçebilirsiniz (kahvaltı 08:00, öğle 13:00, akşam 19:00)

---

### ✅ 2. TARİH ARALIĞI İLE HAFTALIK RAPOR
İstediğiniz tarih aralığında raporları görüntüleyebilirsiniz!

**Nasıl Kullanılır:**
1. Sağ sütunda **"Başlangıç Tarihi"** seçin (örn: 1 Ocak 2025)
2. **"Bitiş Tarihi"** seçin (örn: 7 Ocak 2025)
3. "Seçili Kullanıcının Takip Raporu" butonuna basın

**Örnekler:**
- Son 3 günü görmek için: 3 gün öncesi → Bugün
- Ocak ayının tamamını görmek için: 1 Ocak → 31 Ocak
- Belirli bir haftayı görmek için: Pazartesi → Pazar

---

### ✅ 3. KULLANICIYA ÖZEL LOG SİSTEMİ
Her kullanıcının verileri **tamamen ayrı** saklanıyor!

**Nasıl Çalışır:**
- Sol panelden kullanıcı seçtiğinizde, **sadece o kullanıcıya ait** veriler gösterilir
- Her kullanıcı için ayrı:
  - Yemek kayıtları
  - Kalori hesaplamaları
  - Haftalık grafikler
  - Makro besin analizleri

**Test Etmek İçin:**
1. Sol panelden "Demo BERKAY" seçin → Yemek ekleyin
2. Başka bir kullanıcı seçin (örn: SimUser_2) → Kendi verileri görünür
3. Tekrar "Demo BERKAY"a dönün → Sadece onun kayıtları listelenir ✅

---

## 🔧 DÜZELTİLEN SORUNLAR

### ❌ Problem 1: Buton Kaybolma Sorunu
**Eski Durum:** Haftalık rapor butonuna basınca diğer butonlar kayboluyordu
**✅ Çözüm:** Her butona benzersiz `key` değerleri eklendi. Artık butonlar kaybolmuyor!

### ❌ Problem 2: Tarih Kontrolü Yoktu
**Eski Durum:** Yemekler sadece o anki zamanla kaydediliyordu
**✅ Çözüm:** Manuel tarih/saat girişi eklendi. İstediğiniz tarihe kayıt yapabilirsiniz!

### ❌ Problem 3: Sabit 7 Günlük Rapor
**Eski Durum:** Sadece son 7 günü görebiliyordunuz
**✅ Çözüm:** Tarih aralığı seçici eklendi. İstediğiniz aralığı görebilirsiniz!

---

## 📋 ADIM ADIM KULLANIM

### 🥗 Yemek Ekleme (Elle Tarih Girişi ile)

1. **Sol Panelden Kullanıcı Seçin**
   - Açılır menüden kullanıcıyı seçin (örn: Demo BERKAY)

2. **Tarih ve Saat Belirleyin**
   - Tarih Seçin: `15/01/2025` (takvimden seçin)
   - Saat Seçin: `12:30` (saat ve dakikayı ayarlayın)

3. **Fotoğraf Yükleyin**
   - "Bir yemek fotoğrafı yükleyin" → Fotoğrafı seçin

4. **Analiz ve Kaydet**
   - "Analiz Yap ve KAYDET" butonuna basın
   - Yapay zeka yemeği tanıyacak ve seçtiğiniz tarih/saatle kaydedecek ✅

---

### 📊 Haftalık Rapor Görüntüleme (Tarih Aralığı ile)

1. **Sağ Sütuna Geçin**
   - "Analiz ve Raporlar" bölümüne bakın

2. **Tarih Aralığı Belirleyin**
   - Başlangıç Tarihi: `01/01/2025`
   - Bitiş Tarihi: `07/01/2025`
   - Sistem otomatik olarak kaç gün olduğunu gösterir

3. **Raporu Oluştur**
   - "Seçili Kullanıcının Takip Raporu" butonuna basın
   - Seçili tarih aralığındaki tüm veriler grafiklenecek 📈

---

## 🎯 KULLANIM ÖRNEKLERİ

### Örnek 1: Geçmişe Yemek Ekleme
```
Senaryo: Dün akşam yediğiniz pizzayı bugün eklemek istiyorsunuz

1. Tarih: 14/01/2025 (dün)
2. Saat: 19:30
3. Pizza fotoğrafını yükleyin
4. "Analiz Yap ve KAYDET"
✅ Pizza 14 Ocak 19:30'da kaydedilir!
```

### Örnek 2: Tam Bir Günü Kaydetme
```
Senaryo: Bugünün tüm öğünlerini kaydetmek istiyorsunuz

KAHVALTI:
- Tarih: 15/01/2025, Saat: 08:00
- Fotoğraf: Yumurta + Ekmek
- KAYDET

ÖĞLE:
- Tarih: 15/01/2025, Saat: 13:00
- Fotoğraf: Salata
- KAYDET

AKŞAM:
- Tarih: 15/01/2025, Saat: 19:30
- Fotoğraf: Tavuk + Pilav
- KAYDET

✅ Günün tüm öğünleri kaydedildi!
```

### Örnek 3: Aylık Analiz
```
Senaryo: Ocak ayının tamamını analiz etmek istiyorsunuz

1. Başlangıç: 01/01/2025
2. Bitiş: 31/01/2025
3. "Seçili Kullanıcının Takip Raporu"
✅ Ocak ayının grafiği ve istatistikleri görünür!
```

---

## 💡 İPUÇLARI

### ✅ Log Sistemi Doğru Çalışıyor mu?
- Her kullanıcı için ayrı kayıt tutuluyor ✓
- Manuel tarih ile kayıt yapılabiliyor ✓
- Geçmiş tarihlere veri eklenebiliyor ✓

### ✅ Butonlar Kaybolmuyor
- Her buton benzersiz ID'ye sahip ✓
- Streamlit state management düzeltildi ✓

### ✅ Tarih Kontrolü
- Başlangıç > Bitiş ise uyarı veriyor ✓
- Tarih aralığı gün sayısı gösteriliyor ✓

---

## ❓ SSS (Sık Sorulan Sorular)

**S: Geçmişe yemek ekleyebilir miyim?**
C: Evet! Tarih seçicide istediğiniz tarihi seçebilirsiniz.

**S: Birden fazla kullanıcı aynı anda kullanabilir mi?**
C: Evet! Her kullanıcı kendi verilerini görür, karışma olmaz.

**S: Haftalık raporda veri görünmüyorsa?**
C: Tarih aralığını kontrol edin. O tarihlerde kayıt yoksa "kayıt bulunamadı" uyarısı verir.

**S: Butonlar neden bazen kayboluyordu?**
C: Streamlit'in state management problemi vardı. Artık düzeltildi, tüm butonlar her zaman görünür.

---

## 🚀 HIZLI BAŞLANGIÇ

```bash
# 1. Uygulamayı başlat
streamlit run app.py

# 2. Tarayıcıda aç
http://localhost:8501

# 3. İlk kullanım:
- Sol panelden kullanıcı seç
- Tarih/saat ayarla
- Fotoğraf yükle
- Analiz yap
- Raporu görüntüle
```

---

## 📞 DESTEK

Sorun yaşarsanız:
1. Uygulamayı yeniden başlatın: `Ctrl+C` → `streamlit run app.py`
2. Veritabanını sıfırlayın: `python -m backend.database`
3. Tarayıcı önbelleğini temizleyin: `Ctrl+Shift+R` veya `Cmd+Shift+R`

---

## 🎉 SONUÇ

Tüm istediğiniz özellikler eklendi:
- ✅ Elle tarih/saat girişi
- ✅ Tarih aralığı ile rapor
- ✅ Kullanıcıya özel log sistemi
- ✅ Buton kaybolma sorunu düzeltildi

**Keyifli kullanımlar!** 🍽️
