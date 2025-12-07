import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import os
from PIL import Image
from datetime import datetime, timedelta
import cv2
import sys

# YOL DÜZELTMESİ
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.analiz import analyze_food_image
from backend.database import hesapla_gunluk_kalori, save_user_profile, get_demo_user_id, save_log, get_all_users_profiles 

# --- 1. VERİTABANI VE VERİ ÇEKME MANTIĞI ---

def connect_db():
    return sqlite3.connect('backend/nutrition_data.db')

def get_data(user_id=None, include_simulation=False, days_to_look_back=7):
    """Veriyi çeker. days_to_look_back süresi için filtreler."""
    bag = connect_db()
    
    logs_df = pd.read_sql_query("SELECT * FROM logs", bag)
    foods_df = pd.read_sql_query("SELECT name, calories, protein, carbs, fat, category FROM foods", bag)
    users_df = pd.read_sql_query("SELECT id, name, gender, goal_calories, activity_level, age, goal_type FROM users", bag)
    
    bag.close()
    
    if logs_df.empty:
        return pd.DataFrame()
    
    # Verileri birleştirme (Join)
    merged_df = pd.merge(logs_df, foods_df, left_on='food_name', right_on='name', how='left', suffixes=('_log', '_food'))
    merged_df.rename(columns={'calories_food': 'calories', 'category': 'category_food', 'protein_food': 'protein', 'carbs_food': 'carbs', 'fat_food': 'fat'}, inplace=True)
    final_df = pd.merge(merged_df, users_df, left_on='user_id', right_on='id', how='left', suffixes=('_log', '_user'))
    
    final_df['timestamp'] = pd.to_datetime(final_df['timestamp'])
    final_df['time_hour'] = final_df['timestamp'].dt.hour
    
    # ZAMAN FİLTRESİ: Haftalık (7 gün) veya Simülasyon (30 gün)
    look_back_days = 30 if include_simulation else days_to_look_back
    time_limit = datetime.now() - timedelta(days=look_back_days)
    recent_df = final_df[final_df['timestamp'] >= time_limit].copy()

    # Kullanıcıya göre filtreleme (Canlı Takip)
    if not include_simulation and user_id is not None:
        recent_df = recent_df[recent_df['user_id'] == user_id].copy()

    return recent_df

# --- 2. GRAFİK VE ANALİZ MANTIĞI ---

def create_reports(df, report_type):
    """Pandas ile haftalık ve korelasyon analizlerini yapar."""
    
    if df.empty:
        st.warning("Analiz için yeterli kayıt bulunamadı.")
        return

    # KORELASYON ANALİZİ (Genel Simülasyon Verisi)
    if report_type == "KORELASYON":
        st.header("🔬 Genel Korelasyon Analizi (5000+ Kayıt)")
        
        # 1. Sabah Karbonhidrat Tüketimi
        carb_classes = ['Karbonhidrat Kaynağı', 'Unlu Mamul'] 
        morning_carbs = df[
            (df['time_hour'] >= 6) & (df['time_hour'] <= 12) & (df['category_food'].isin(carb_classes))
        ]
        gender_carb_analysis = morning_carbs.groupby('gender').size().reset_index(name='Sabah Tüketimi')
        st.dataframe(gender_carb_analysis, use_container_width=True)
        
        if 'Kadın' in gender_carb_analysis['gender'].values and 'Erkek' in gender_carb_analysis['gender'].values:
            kadin_tuketim = gender_carb_analysis[gender_carb_analysis['gender'] == 'Kadın']['Sabah Tüketimi'].iloc[0]
            erkek_tuketim = gender_carb_analysis[gender_carb_analysis['gender'] == 'Erkek']['Sabah Tüketimi'].iloc[0]
            
            if kadin_tuketim > erkek_tuketim:
                st.success(f"Analiz Sonucu: Simülasyon verisinde **Kadınların sabah karbonhidrat tüketimi** erkeklere göre daha fazladır.")
            else:
                st.info(f"Analiz Sonucu: Simülasyon verisinde **Erkekler daha fazla karbonhidrat tüketmiştir**.")
        
        # 2. Yaşa Göre Fast-Food Oranı
        st.markdown("---")
        st.markdown("### Yaşa Göre Fast-Food Oranı")
        df['Age Group'] = pd.cut(df['age'], bins=[18, 30, 50, 80], labels=['Genç (18-30)', 'Orta Yaş (31-50)', 'Yaşlı (50+)'])
        fast_food_consumption = df.groupby('Age Group')['category_food'].value_counts(normalize=True).mul(100).rename('Yuzde').reset_index()
        fast_food_only = fast_food_consumption[fast_food_consumption['category_food'] == 'Fast-Food']
        st.bar_chart(fast_food_only, x='Age Group', y='Yuzde')


    # HAFTALIK TAKİP RAPORU (Kişiye Özel Canlı Veri)
    elif report_type == "HAFTALIK":
        st.header("📈 Haftalık Tüketim Takibi")
        
        # Kalori Takibi
        daily_summary = df.groupby(df['timestamp'].dt.date)['calories'].sum().reset_index()
        daily_summary.columns = ['Tarih', 'Toplam Kalori']
        
        st.line_chart(daily_summary.set_index('Tarih'), height=250)
        
        # MAKRO BESİN DAĞILIMI (Protein/Karb/Yağ) - TALEP EDİLEN GRAFİK
        st.markdown("---")
        st.markdown("### Makro Besin Daşılımı (Toplam Gram)")
        macro_totals = pd.DataFrame({
            'Besin': ['Protein', 'Karbonhidrat', 'Yağ'],
            'Gram': [df['protein'].sum(), df['carbs'].sum(), df['fat'].sum()]
        })
        st.bar_chart(macro_totals.set_index('Besin'), height=300)


# --- 3. ANA ARAYÜZ DÜZENİ ---

def user_input_form():
    """Kullanıcıdan yaş, kilo, cinsiyet gibi verileri alır ve hedefi hesaplar."""
    with st.sidebar:
        st.header("👤 Kullanıcı Profili ve Seçim")
        
        all_users_df = get_all_users_profiles()
        user_map = dict(zip(all_users_df['id'], all_users_df['name']))
        
        selected_name = st.selectbox("1. Görüntülenecek Kullanıcıyı Seçin:", list(user_map.values()), index=0)
        selected_user_id = list(user_map.keys())[list(user_map.values()).index(selected_name)]
        
        current_profile = all_users_df[all_users_df['id'] == selected_user_id].iloc[0]

        st.markdown("---")
        st.markdown("2. Profili Güncelle")
        name = st.text_input("Ad Soyad", value=current_profile['name'])
        gender = st.selectbox("Cinsiyet", ["Erkek", "Kadın"], index=0 if current_profile['gender'] == 'Erkek' else 1)
        age = st.slider("Yaş", 18, 80, current_profile['age'])
        
        weight = st.slider("Kilo (kg)", 40.0, 150.0, float(current_profile['weight']), step=0.5) 
        height = st.slider("Boy (cm)", 140, 220, int(current_profile['height']))
        
        activity_levels = ["Hareketsiz", "Az Hareketli", "Orta Hareketli", "Çok Hareketli", "Sporcu"]
        activity = st.selectbox("Aktivite Düzeyi", activity_levels, index=activity_levels.index(current_profile['activity_level']) if current_profile['activity_level'] in activity_levels else 2)
        goal = st.selectbox("Hedef", ["Kilo Koru", "Kilo Ver", "Kilo Al"], index=2 if current_profile['goal_type'] == 'Kilo Al' else (1 if current_profile['goal_type'] == 'Kilo Ver' else 0))

        calculated_goal = hesapla_gunluk_kalori(weight, height, age, gender, activity, goal)
        st.info(f"Hesaplanan Hedef Kalori: **{calculated_goal} kcal**")
        
        if st.button("Profili Güncelle/Kaydet", key="update_profile"):
            save_user_profile(selected_user_id, name, gender, age, weight, height, activity, goal, calculated_goal)
            st.success(f"✅ Kullanıcı {selected_name} (ID: {selected_user_id}) profili güncellendi!")
            
    return selected_user_id 

def main_app():
    st.set_page_config(layout="wide")
    st.title("🍽️ GÖRSEL BESİN ANALİZ SİSTEMİ")
    st.subheader("Final Projesi: YOLOv8 Nesne Tespiti ve Besin Takibi")

    user_id = user_input_form()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("## 📷 Tespit ve Kayıt")
        uploaded_file = st.file_uploader("1. Bir yemek fotoğrafı yükleyin:", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Yüklenen Resim', use_column_width=True)
            
            test_images_dir = os.path.join("backend", "test_images") 
            os.makedirs(test_images_dir, exist_ok=True) 
            image_path = os.path.join(test_images_dir, uploaded_file.name)

            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # TEK BUTON İLE ANALİZ YAP, KAYDET VE KİŞİSEL RAPORU GÖSTER
            if st.button("2. Analiz Yap ve KAYDET"):
                with st.spinner("Yapay Zeka Analiz Ediyor..."):
                    results_df = analyze_food_image(image_path=image_path)
                    
                    # KRİTİK KONTROL: Kalori sütunu var mı?
                    if 'Kalori' not in results_df.columns:
                        st.error("❌ Tespit Hatası! Yapay Zeka resimde bir şey bulamadı veya resim bozuk.")
                        st.dataframe(results_df, use_container_width=True)
                        return 
                    
                    st.success("✅ Analiz Tamamlandı!")
                    st.dataframe(results_df, use_container_width=True)
                    
                    # LOG KAYDI
                    if not results_df.empty:
                        for index, row in results_df.iterrows():
                            if row['Kalori'] != 'Veri Eksik':
                                save_log(user_id=user_id, food_name=row['Yemek'])
                        st.success("Log Kaydı Yapıldı! Haftalık rapor güncellendi.")

                # --- KİŞİSEL RAPORU ANINDA GÖSTERME ---
                st.markdown("---")
                user_logs_df = get_data(user_id=user_id, include_simulation=False, days_to_look_back=7) # 7 GÜNLÜK FİLTRE BURADA!
                create_reports(user_logs_df, "HAFTALIK")


    # SÜTUN 2: GENEL RAPORLAR
    with col2:
        st.markdown("## 📈 Analiz ve Raporlar")
        
        # KİŞİYE ÖZEL HAFTALIK RAPOR (Manuel Yenileme)
        if st.button("3. Seçili Kullanıcının Takip Raporu"):
            with st.spinner(f"Kullanıcı ID: {user_id}'e Ait Kayıtlar Analiz Ediliyor..."):
                user_logs_df = get_data(user_id=user_id, include_simulation=False, days_to_look_back=7) # 7 GÜNLÜK FİLTRE BURADA!
                create_reports(user_logs_df, "HAFTALIK")

        st.markdown("---")
        # GENEL KORELASYON ANALİZİ
        if st.button("Genel Korelasyon Analizi (Hoca Raporu)"):
            with st.spinner("5000+ Simülasyon Kaydı Analiz Ediliyor..."):
                sim_df = get_data(include_simulation=True, days_to_look_back=30) # KORELASYON İÇİN 30 GÜNLÜK VERİ ÇEKİLİR
                create_reports(sim_df, "KORELASYON")


if __name__ == "__main__":
    try:
        main_app()
    except Exception as e:
        st.error(f"❌ Bir hata oluştu: {str(e)}")
        st.exception(e)