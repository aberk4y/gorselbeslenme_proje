#!/bin/bash

echo "=== GitHub'a Kaydetme İşlemi Başlıyor ==="

cd /app

# Değişiklikleri göster
echo ""
echo "📋 Değişen Dosyalar:"
git status --short

# Tüm değişiklikleri ekle
echo ""
echo "➕ Dosyalar ekleniyor..."
git add app.py backend/database.py KULLANIM_KILAVUZU.md DEGISIKLIK_LISTESI.md TEST_CHECKLIST.md requirements.txt README.md

# Commit yap
echo ""
echo "💾 Commit yapılıyor..."
git config user.name "Berkay" 
git config user.email "your-email@example.com"
git commit -m "v2.0: Manuel tarih girişi, tarih aralığı seçici ve buton düzeltmeleri eklendi"

# Push yap (bu adımı kendiniz yapmalısınız)
echo ""
echo "🚀 GitHub'a göndermek için:"
echo "git push origin main"
echo ""
echo "veya"
echo "git push"

