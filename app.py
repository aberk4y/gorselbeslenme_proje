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
        st.header("🔬 Gelişmiş Korelasyon Analizi")
        st.info(f"📊 Toplam {len(df)} kayıt analiz ediliyor")
        
        # 1. CİNSİYETE GÖRE HEDEF BAŞARI ANALİZİ
        st.markdown("---")
        st.markdown("### 🎯 Cinsiyet Bazlı Hedef Başarı Oranı")
        
        # Her kullanıcının 7 günlük verisi için hesaplama
        user_goal_success = []
        for user_id in df['user_id'].unique():
            user_data = df[df['user_id'] == user_id]
            if not user_data.empty:
                total_consumed = user_data['calories'].sum()
                goal_calories = user_data['goal_calories'].iloc[0]
                days = user_data['timestamp'].dt.date.nunique()
                expected_total = goal_calories * days
                
                # Hedef tipi
                goal_type = user_data['goal_type'].iloc[0]
                gender = user_data['gender'].iloc[0]
                
                # Başarı kriterleri
                if goal_type == "Kilo Ver":
                    # Kalori açığı olmalı (hedeften az yemeli)
                    success = total_consumed < expected_total
                elif goal_type == "Kilo Al":
                    # Kalori fazlası olmalı (hedeften fazla yemeli)
                    success = total_consumed > expected_total
                else:  # Kilo Koru
                    # ±%10 tolerans ile hedefe yakın olmalı
                    success = abs(total_consumed - expected_total) / expected_total < 0.1
                
                user_goal_success.append({
                    'user_id': user_id,
                    'gender': gender,
                    'goal_type': goal_type,
                    'success': success
                })
        
        success_df = pd.DataFrame(user_goal_success)
        
        if not success_df.empty:
            gender_success = success_df.groupby('gender')['success'].agg(['sum', 'count'])
            gender_success['success_rate'] = (gender_success['sum'] / gender_success['count'] * 100).round(1)
            
            st.dataframe(gender_success[['success_rate']].rename(columns={'success_rate': 'Başarı Oranı (%)'}), use_container_width=True)
            
            if 'Kadın' in gender_success.index and 'Erkek' in gender_success.index:
                kadin_success = gender_success.loc['Kadın', 'success_rate']
                erkek_success = gender_success.loc['Erkek', 'success_rate']
                
                if kadin_success > erkek_success:
                    st.success(f"✅ **Kadınlar daha başarılı!** Kadınların %{kadin_success:.1f}'i hedefe ulaşırken, erkeklerin %{erkek_success:.1f}'i hedefe ulaştı.")
                else:
                    st.success(f"✅ **Erkekler daha başarılı!** Erkeklerin %{erkek_success:.1f}'i hedefe ulaşırken, kadınların %{kadin_success:.1f}'i hedefe ulaştı.")
        
        # 2. SABAH SAATLERİNDE CİNSİYETE GÖRE PROTEİN TÜKETİMİ
        st.markdown("---")
        st.markdown("### 🥩 Sabah Saatlerinde Cinsiyet Bazlı Protein Tüketimi")
        
        morning_data = df[(df['time_hour'] >= 6) & (df['time_hour'] <= 12)]
        
        if not morning_data.empty:
            gender_protein = morning_data.groupby('gender')['protein'].sum().reset_index()
            gender_protein.columns = ['Cinsiyet', 'Toplam Protein (g)']
            
            st.dataframe(gender_protein, use_container_width=True)
            st.bar_chart(gender_protein.set_index('Cinsiyet'), height=300)
            
            if len(gender_protein) == 2:
                kadin_protein = gender_protein[gender_protein['Cinsiyet'] == 'Kadın']['Toplam Protein (g)'].iloc[0]
                erkek_protein = gender_protein[gender_protein['Cinsiyet'] == 'Erkek']['Toplam Protein (g)'].iloc[0]
                
                if kadin_protein > erkek_protein:
                    fark = kadin_protein - erkek_protein
                    st.info(f"📊 Kadınlar sabah saatlerinde erkeklere göre **{fark:.0f}g daha fazla protein** tüketti.")
                else:
                    fark = erkek_protein - kadin_protein
                    st.info(f"📊 Erkekler sabah saatlerinde kadınlara göre **{fark:.0f}g daha fazla protein** tüketti.")
        
        # 3. HEDEF TİPİNE GÖRE ORTALAMA KALORI FARKI
        st.markdown("---")
        st.markdown("### 🎯 Hedef Tipi Bazlı Performans")
        
        goal_performance = []
        for goal_type in df['goal_type'].unique():
            goal_data = df[df['goal_type'] == goal_type]
            users = goal_data['user_id'].unique()
            
            for user_id in users:
                user_data = goal_data[goal_data['user_id'] == user_id]
                total_consumed = user_data['calories'].sum()
                goal_calories = user_data['goal_calories'].iloc[0]
                days = user_data['timestamp'].dt.date.nunique()
                expected_total = goal_calories * days
                
                diff = total_consumed - expected_total
                goal_performance.append({
                    'goal_type': goal_type,
                    'calorie_diff': diff
                })
        
        perf_df = pd.DataFrame(goal_performance)
        if not perf_df.empty:
            avg_diff = perf_df.groupby('goal_type')['calorie_diff'].mean().round(0)
            st.dataframe(avg_diff.rename('Ortalama Kalori Farkı (kcal)'), use_container_width=True)
            
            st.write("**Yorum:**")
            for goal, diff in avg_diff.items():
                if diff > 0:
                    st.warning(f"- {goal}: Ortalama {abs(diff):.0f} kcal **fazla** tüketim")
                elif diff < 0:
                    st.success(f"- {goal}: Ortalama {abs(diff):.0f} kcal **açık**")
                else:
                    st.info(f"- {goal}: Hedefle **tam uyumlu**")
        
        # 4. YAŞA GÖRE FAST-FOOD TÜKETİMİ
        st.markdown("---")
        st.markdown("### 🍔 Yaş Gruplarına Göre Fast-Food Tüketimi")
        
        df['Age Group'] = pd.cut(df['age'], bins=[18, 30, 50, 80], labels=['Genç (18-30)', 'Orta Yaş (31-50)', 'Yaşlı (50+)'])
        fast_food_data = df[df['category_food'] == 'Fast-Food']
        
        if not fast_food_data.empty:
            age_ff = fast_food_data.groupby('Age Group').size().reset_index(name='Tüketim Sayısı')
            st.dataframe(age_ff, use_container_width=True)
            st.bar_chart(age_ff.set_index('Age Group'), height=300)


    # HAFTALIK TAKİP RAPORU (Kişiye Özel Canlı Veri)
    elif report_type == "HAFTALIK":
        st.header("📈 Haftalık Tüketim Takibi")
        
        # Kalori Takibi
        daily_summary = df.groupby(df['timestamp'].dt.date)['calories'].sum().reset_index()
        daily_summary.columns = ['Tarih', 'Toplam Kalori']
        
        st.line_chart(daily_summary.set_index('Tarih'), height=250)
        
        # MAKRO BESİN DAĞILIMI - PASTA GRAFİK
        st.markdown("---")
        st.markdown("### 🥧 Makro Besin Dağılımı (Haftalık)")
        
        total_protein = df['protein'].sum()
        total_carbs = df['carbs'].sum()
        total_fat = df['fat'].sum()
        
        import plotly.graph_objects as go
        
        fig = go.Figure(data=[go.Pie(
            labels=['Protein', 'Karbonhidrat', 'Yağ'],
            values=[total_protein, total_carbs, total_fat],
            hole=.3,
            marker=dict(colors=['#FF6B6B', '#4ECDC4', '#FFE66D'])
        )])
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # HAFTALIK ANALİZ YORUMU
        st.markdown("---")
        st.markdown("### 💬 Haftalık Analiz Yorumu")
        
        # Toplam kalori hesapla
        total_calories_consumed = df['calories'].sum()
        
        # Kullanıcı bilgileri (ilk satırdan al)
        if not df.empty:
            user_goal_calories = df['goal_calories'].iloc[0]
            user_goal_type = df['goal_type'].iloc[0]
            days_count = df['timestamp'].dt.date.nunique()
            
            # Haftalık hedef kalori
            weekly_goal = user_goal_calories * days_count
            calorie_diff = total_calories_consumed - weekly_goal
            
            # Kategori bazlı yorum
            st.info(f"📊 **Hedef Kategoriniz:** {user_goal_type}")
            st.metric("Toplam Kalori Alımı", f"{total_calories_consumed:,.0f} kcal")
            st.metric("Haftalık Hedef", f"{weekly_goal:,.0f} kcal")
            
            if calorie_diff > 0:
                st.warning(f"⚠️ **Kalori Fazlası:** {abs(calorie_diff):,.0f} kcal")
                
                if user_goal_type == "Kilo Ver":
                    st.error("❌ **Dikkat!** Kilo verme hedefiniz var ama kalori fazlası oluşturdunuz. Hedeften sapma var!")
                elif user_goal_type == "Kilo Al":
                    st.success("✅ **Harika!** Kilo alma hedefinize uygun şekilde kalori fazlası oluşturdunuz!")
                else:  # Kilo Koru
                    st.warning("⚠️ Kilo koruma hedefiniz var. Kalori fazlası oluşturdunuz, dikkatli olun!")
                    
            elif calorie_diff < 0:
                st.success(f"✅ **Kalori Açığı:** {abs(calorie_diff):,.0f} kcal")
                
                if user_goal_type == "Kilo Ver":
                    st.success("✅ **Tebrikler!** Kilo verme hedefinize uygun kalori açığı oluşturdunuz!")
                elif user_goal_type == "Kilo Al":
                    st.error("❌ **Dikkat!** Kilo alma hedefiniz var ama kalori açığı oluşturdunuz. Daha fazla yemelisiniz!")
                else:  # Kilo Koru
                    st.info("ℹ️ Kilo koruma hedefiniz var. Hafif kalori açığı oluşturdunuz.")
            else:
                st.success("🎯 **Mükemmel!** Hedef kalorinize tam ulaştınız!")
            
            # Günlük ortalama
            daily_avg = total_calories_consumed / days_count
            st.info(f"📅 Günlük Ortalama: {daily_avg:,.0f} kcal ({days_count} gün)")
        
        # Makro besin oranları
        st.markdown("---")
        st.markdown("### 📊 Makro Besin Oranları")
        total_macro = total_protein + total_carbs + total_fat
        if total_macro > 0:
            st.write(f"🥩 Protein: {(total_protein/total_macro*100):.1f}% ({total_protein:.0f}g)")
            st.write(f"🍞 Karbonhidrat: {(total_carbs/total_macro*100):.1f}% ({total_carbs:.0f}g)")
            st.write(f"🧈 Yağ: {(total_fat/total_macro*100):.1f}% ({total_fat:.0f}g)")


# --- 3. ANA ARAYÜZ DÜZENİ ---

def user_input_form():
    """Kullanıcıdan yaş, kilo, cinsiyet gibi verileri alır ve hedefi hesaplar."""
    with st.sidebar:
        st.header("👤 Kullanıcı Yönetimi")
        
        # YENİ KULLANICI EKLEME BÖLÜMÜ
        with st.expander("➕ Yeni Kullanıcı Ekle"):
            st.markdown("### Yeni Kullanıcı Bilgileri")
            new_name = st.text_input("Ad Soyad", key="new_user_name")
            new_gender = st.selectbox("Cinsiyet", ["Erkek", "Kadın"], key="new_user_gender")
            new_age = st.slider("Yaş", 18, 80, 25, key="new_user_age")
            new_weight = st.slider("Kilo (kg)", 40.0, 150.0, 70.0, step=0.5, key="new_user_weight")
            new_height = st.slider("Boy (cm)", 140, 220, 170, key="new_user_height")
            
            activity_levels = ["Hareketsiz", "Az Hareketli", "Orta Hareketli", "Çok Hareketli", "Sporcu"]
            new_activity = st.selectbox("Aktivite Düzeyi", activity_levels, index=2, key="new_user_activity")
            new_goal = st.selectbox("Hedef", ["Kilo Koru", "Kilo Ver", "Kilo Al"], key="new_user_goal")
            
            new_calculated_goal = hesapla_gunluk_kalori(new_weight, new_height, new_age, new_gender, new_activity, new_goal)
            st.info(f"Hedef Kalori: **{new_calculated_goal} kcal**")
            
            if st.button("✅ Kullanıcıyı Ekle", key="add_new_user"):
                if new_name.strip():
                    # Yeni kullanıcı ID'si (en büyük ID + 1)
                    all_users = get_all_users_profiles()
                    new_id = all_users['id'].max() + 1 if not all_users.empty else 1
                    
                    save_user_profile(new_id, new_name, new_gender, new_age, new_weight, new_height, 
                                    new_activity, new_goal, new_calculated_goal)
                    st.success(f"🎉 {new_name} başarıyla eklendi! (ID: {new_id})")
                    st.rerun()
                else:
                    st.error("❌ Lütfen ad soyad girin!")
        
        st.markdown("---")
        
        # MEVCUT KULLANICI SEÇİMİ VE GÜNCELLEME
        all_users_df = get_all_users_profiles()
        user_map = dict(zip(all_users_df['id'], all_users_df['name']))
        
        selected_name = st.selectbox("1. Kullanıcı Seçin:", list(user_map.values()), index=0)
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
        
        if st.button("💾 Profili Güncelle", key="update_profile"):
            save_user_profile(selected_user_id, name, gender, age, weight, height, activity, goal, calculated_goal)
            st.success(f"✅ {selected_name} profili güncellendi!")
            
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
            
            # MANUEL TARİH VE SAAT GİRİŞİ
            st.markdown("### 📅 Tarih ve Saat Bilgisi")
            col_date, col_time = st.columns(2)
            
            with col_date:
                log_date = st.date_input("Tarih Seçin:", value=datetime.now().date(), key="log_date")
            
            with col_time:
                log_time = st.time_input("Saat Seçin:", value=datetime.now().time(), key="log_time")
            
            # Tarih ve saati birleştir
            selected_datetime = datetime.combine(log_date, log_time)
            st.info(f"📌 Seçilen Zaman: {selected_datetime.strftime('%d/%m/%Y %H:%M')}")

            # TEK BUTON İLE ANALİZ YAP, KAYDET VE KİŞİSEL RAPORU GÖSTER
            if st.button("2. Analiz Yap ve KAYDET", key="analyze_button"):
                with st.spinner("Yapay Zeka Analiz Ediyor..."):
                    results_df = analyze_food_image(image_path=image_path)
                    
                    # KRİTİK KONTROL: Kalori sütunu var mı?
                    if 'Kalori' not in results_df.columns:
                        st.error("❌ Tespit Hatası! Yapay Zeka resimde bir şey bulamadı veya resim bozuk.")
                        st.dataframe(results_df, use_container_width=True)
                    else:
                        st.success("✅ Analiz Tamamlandı!")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # LOG KAYDI - Manuel tarih ile
                        if not results_df.empty:
                            custom_timestamp = selected_datetime.strftime('%Y-%m-%d %H:%M:%S')
                            for index, row in results_df.iterrows():
                                if row['Kalori'] != 'Veri Eksik':
                                    save_log(user_id=user_id, food_name=row['Yemek'], custom_timestamp=custom_timestamp)
                            st.success(f"✅ Log Kaydı Yapıldı! (Kullanıcı ID: {user_id}, Tarih: {selected_datetime.strftime('%d/%m/%Y %H:%M')})")


    # SÜTUN 2: GENEL RAPORLAR
    with col2:
        st.markdown("## 📈 Analiz ve Raporlar")
        
        # TARİH ARALIĞI SEÇİCİ İLE HAFTALIK RAPOR
        st.markdown("### 📊 Haftalık Takip Raporu")
        
        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input(
                "Başlangıç Tarihi:", 
                value=datetime.now().date() - timedelta(days=7),
                key="start_date"
            )
        
        with col_end:
            end_date = st.date_input(
                "Bitiş Tarihi:", 
                value=datetime.now().date(),
                key="end_date"
            )
        
        # Tarih aralığı kontrolü
        if start_date > end_date:
            st.error("⚠️ Başlangıç tarihi, bitiş tarihinden büyük olamaz!")
        else:
            days_diff = (end_date - start_date).days
            st.info(f"📅 Seçilen Aralık: {days_diff + 1} gün ({start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')})")
        
        # KİŞİYE ÖZEL HAFTALIK RAPOR (Manuel Yenileme)
        if st.button("3. Seçili Kullanıcının Takip Raporu", key="weekly_report_button"):
            if start_date <= end_date:
                with st.spinner(f"Kullanıcı ID: {user_id}'e Ait Kayıtlar Analiz Ediliyor..."):
                    # Özel tarih aralığı ile veri çekme
                    bag = connect_db()
                    start_datetime = datetime.combine(start_date, datetime.min.time())
                    end_datetime = datetime.combine(end_date, datetime.max.time())
                    
                    query = """
                        SELECT logs.*, foods.calories, foods.protein, foods.carbs, foods.fat, foods.category,
                               users.name, users.gender, users.age, users.goal_calories, users.activity_level, users.goal_type
                        FROM logs
                        LEFT JOIN foods ON logs.food_name = foods.name
                        LEFT JOIN users ON logs.user_id = users.id
                        WHERE logs.user_id = ? AND logs.timestamp BETWEEN ? AND ?
                    """
                    
                    user_logs_df = pd.read_sql_query(
                        query, 
                        bag, 
                        params=(user_id, start_datetime.strftime('%Y-%m-%d %H:%M:%S'), end_datetime.strftime('%Y-%m-%d %H:%M:%S'))
                    )
                    bag.close()
                    
                    if not user_logs_df.empty:
                        user_logs_df['timestamp'] = pd.to_datetime(user_logs_df['timestamp'])
                        user_logs_df['time_hour'] = user_logs_df['timestamp'].dt.hour
                        user_logs_df.rename(columns={'category': 'category_food'}, inplace=True)
                        create_reports(user_logs_df, "HAFTALIK")
                    else:
                        st.warning(f"⚠️ Seçili tarih aralığında (Kullanıcı ID: {user_id}) hiç kayıt bulunamadı!")

        st.markdown("---")
        # GENEL KORELASYON ANALİZİ
        if st.button("Genel Korelasyon Analizi (Hoca Raporu)", key="correlation_button"):
            with st.spinner("5000+ Simülasyon Kaydı Analiz Ediliyor..."):
                sim_df = get_data(include_simulation=True, days_to_look_back=30)
                create_reports(sim_df, "KORELASYON")


if __name__ == "__main__":
    try:
        main_app()
    except Exception as e:
        st.error(f"❌ Bir hata oluştu: {str(e)}")
        st.exception(e)