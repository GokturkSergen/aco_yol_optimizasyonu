import streamlit as st  # Web arayüzü
import pandas as pd  # Veri tabloları ve CSV işlemleri için.
from streamlit_folium import st_folium  # Harita ile alakalı her şey

from data.koordinatlar import sehir_koordinatlari 
from core.matris_araclari import mesafe_matrisi_olustur  # Google API ile km matrisi oluşturma
from core.karinca_algoritmasi import kka_calistir 
from visual.gorsellestirme import yakinsama_grafigi_ciz, harita_ciz  
from ayarlar import KKA_AYARLARI  

# --- Sayfa Yapılandırması ---
st.set_page_config(page_title="KKA Yol Optimizasyonu",layout="wide" )  

st.title("Karınca Kolonisi Algoritması ile Yol Optimizasyonu") 
st.subheader("Senaryo 5: Ankara Su Numunesi Toplama Rotası")  

# --- Yan Menü (Sidebar) Ayarları ---
st.sidebar.header("Algoritma Parametreleri")  

# Kullanıcıdan parametreleri almak için kaydırma çubukları (slider) oluştur:
karinca_sayisi = st.sidebar.slider("Karınca Sayısı", 2, 50, KKA_AYARLARI["karinca_sayisi"])  
iterasyon_sayisi = st.sidebar.slider("İterasyon Sayısı", 5, 100, KKA_AYARLARI["iterasyon_sayisi"])  
alpha = st.sidebar.slider("Alpha (Feromon Etkisi)", 0.1, 5.0, KKA_AYARLARI["alpha"])  
beta = st.sidebar.slider("Beta (Mesafe Etkisi)", 0.1, 5.0, KKA_AYARLARI["beta"])  
buharlasma = st.sidebar.slider("Buharlaşma Oranı", 0.0, 1.0, KKA_AYARLARI["buharlasma_orani"])

api_anahtari = st.secrets.get("GOOGLE_API_KEY", None)  # secrets.toml dosyasından şifreli anahtarı oku.

# --- Hafıza (Session State) Yönetimi ---
# Sayfa yenilendiğinde veriler kaybolmasın diye 'session_state' kullanıyoruz.
if 'sonuclar' not in st.session_state:  # Eğer hafızada 'sonuclar' diye bir alan yoksa...
    st.session_state.sonuclar = None  # ...başlangıç değeri olarak boş (None) ata.

# --- Başlat Butonu ---
if st.sidebar.button("Optimizasyonu Başlat"):  # Kullanıcı butona basarsa bu bloğu çalıştır.
    with st.spinner('Rota hesaplanıyor...'):  # Ekranda dönen 'yükleniyor' simgesi göster.
        
        # 1. Adım: Mesafe Matrisini Oluştur
        # Seçilen şehirler ve API anahtarı ile mesafeleri hesapla.
        mesafe_matrisi = mesafe_matrisi_olustur(sehir_koordinatlari, api_anahtari)
        
        # 2. Adım: Algoritmayı Çalıştır
        # Elde edilen mesafe matrisi ve parametrelerle KKA algoritmasını başlat.
        en_iyi_yol, en_iyi_mesafe, iterasyon_gecmisi = kka_calistir(
            mesafe_matrisi,
            karinca_sayisi=karinca_sayisi,
            iterasyon_sayisi=iterasyon_sayisi,
            alpha=alpha,
            beta=beta,
            buharlasma_orani=buharlasma,
            feromon_katkisi=KKA_AYARLARI["feromon_katkisi"]
        )

        # 3. Adım: Sonuçları Hafızaya Kaydet
        
        st.session_state.sonuclar = {
            "en_iyi_yol": en_iyi_yol,  
            "en_iyi_mesafe": en_iyi_mesafe,  
            "iterasyon_gecmisi": iterasyon_gecmisi,  
            "matris_toplami": mesafe_matrisi.sum()  
        }

# --- Sonuçları Ekrana Basma ---
if st.session_state.sonuclar is not None:  # Hafızada veri varsa (daha önce hesaplandıysa)...
    veriler = st.session_state.sonuclar  # Veriyi kısa bir değişkene al.
    
    # Hata Kontrolü: Eğer matris toplamı 0 ise API verisi çekilememiş demektir.
    if veriler["matris_toplami"] == 0:
        st.error("⚠️ Mesafe matrisi oluşturulamadı (0 KM). API kotanızı kontrol edin.")  # Hata mesajı göster.
    else:
        # Ekranı iki sütuna böl (Sol taraf geniş, sağ taraf dar).
        col1, col2 = st.columns([2, 1])

        with col1:  # Sol sütun işlemleri:
            st.success(f"✅ En Kısa Mesafe: {veriler['en_iyi_mesafe']:.2f} km")  # Mesafeyi yeşil kutuda yaz.
            
            # Yol İsimlerini Hazırla
            # İndeks listesini (0, 1, 2) şehir isimlerine ("Mogan", "Eymir"...) çevir.
            rota_isimleri = [sehir_koordinatlari[i][0] for i in veriler['en_iyi_yol']]
            st.write("**Bulunan En İyi Rota:**")  # Başlık yaz.
            st.info(" ➝ ".join(rota_isimleri))  # İsimleri ok işaretiyle birleştirip mavi kutuda göster.
            
            # Haritayı Oluştur ve Göster
            harita_objesi = harita_ciz(veriler['en_iyi_yol'], sehir_koordinatlari)  # Harita objesini oluştur.
            st_folium(harita_objesi, width=700, height=500, returned_objects=[])  # Haritayı ekrana bas.

        with col2:  # Sağ sütun işlemleri:
            st.write("**Yakınsama Grafiği**")  # Grafik başlığı.
            grafik = yakinsama_grafigi_ciz(veriler['iterasyon_gecmisi'])  # Grafiği oluştur.
            st.pyplot(grafik)  # Grafiği çizdir.
            
            # İndirme Butonu Hazırlığı
            # Verileri Excel formatına uygun hale getir.
            df_sonuc = pd.DataFrame({
                "Iterasyon": range(1, len(veriler['iterasyon_gecmisi'])+1), 
                "Mesafe (km)": veriler['iterasyon_gecmisi']
            })
            # CSV indirme butonunu ekle.
            st.download_button("Sonuçları İndir", df_sonuc.to_csv(), "sonuclar.csv")