import requests  # İnternet istekleri için kütüphane.
import numpy as np  # Matematiksel işlemler ve matrisler için kütüphane.
import streamlit as st  # Arayüz uyarıları için.
import pandas as pd  # Veri kaydetme/okuma için.
import os  # Dosya sistemi kontrolü için.

def mesafe_matrisi_olustur(koordinatlar, api_anahtari):
    """
    Google Routes API kullanarak şehirler arası gerçek sürüş mesafelerini çeker.
    """
    
    # --- 1. ÖNBELLEK (CACHE) KONTROLÜ ---
    # Her seferinde API'ye para ödememek için, varsa kayıtlı dosyadan oku.
    kayit_dosyasi = "data/mesafe_matrisi_onbellek.csv"
    if os.path.exists(kayit_dosyasi):  # Dosya var mı?
        try:
            df = pd.read_csv(kayit_dosyasi, index_col=0)  # CSV'yi oku.
            matris = df.values  # Değerleri al.
            if np.sum(matris) > 0:  # Eğer matris boş değilse...
                return matris  # ...kayıtlı matrisi döndür.
        except:
            pass  # Okuma hatası olursa görmezden gel, API'ye geç.

    n = len(koordinatlar)  # Şehir sayısı.
    
    # --- 2. API VERİ PAKETİ HAZIRLIĞI ---
    # Google API'nin istediği formatta durak noktalarını hazırla.
    durak_noktalari = []
    for _, (enlem, boylam) in koordinatlar.values():
        durak_noktalari.append({
            "waypoint": {
                "location": {
                    "latLng": {
                        "latitude": enlem,
                        "longitude": boylam
                    }
                }
            }
        })

    # İstek atılacak Google adresi.
    adres_url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    
    # İstek Başlıkları (Headers)
    # X-Goog-FieldMask: Sadece ihtiyacımız olan 'mesafe' verisini istiyoruz.
    basliklar = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_anahtari,
        "X-Goog-FieldMask": "originIndex,destinationIndex,distanceMeters,status"
    }
    
    # İstek Gövdesi (Payload)
    govde_verisi = {
        "origins": durak_noktalari,       # Başlangıç noktaları.
        "destinations": durak_noktalari,  # Varış noktaları.
        "travelMode": "DRIVE",            # Mod: Sürüş.
        "routingPreference": "TRAFFIC_AWARE" # Trafik durumunu dikkate al.
    }

    # Sonuçları tutacak boş matris (Hepsi 0).
    mesafe_matrisi_km = np.zeros((n, n))

    try:
        # API anahtarı yoksa hata ver.
        if not api_anahtari:
            st.error("❌ API Anahtarı eksik!")
            return mesafe_matrisi_km

        # --- 3. API İSTEĞİ GÖNDER ---
        # yazılanı google'dan isteme
        cevap = requests.post(adres_url, json=govde_verisi, headers=basliklar)
        
        # Veri geldi mi diye kontrol et.
        veri = cevap.json()
        
        # --- 4. GELEN CEVABI İŞLE ---
        for oge in veri:
            # Gelen verideki indeksleri ve mesafeyi al.
            baslangic_idx = oge.get("originIndex")
            varis_idx = oge.get("destinationIndex")
            mesafe_metre = oge.get("distanceMeters")

            # Eğer mesafe verisi başarılı bir şekilde geldiyse:
            if baslangic_idx is not None and varis_idx is not None and mesafe_metre is not None:
                # Metreyi kilometreye çevir ve matrise yaz.
                mesafe_matrisi_km[baslangic_idx][varis_idx] = mesafe_metre / 1000.0
        
        pd.DataFrame(mesafe_matrisi_km).to_csv(kayit_dosyasi)

    except Exception as hata:
        st.error(f"❌ Kod Hatası: {str(hata)}")  # Hata varsa ekrana bas.
        return mesafe_matrisi_km

    # Köşegenleri (kendine gidişleri) sonsuz yap ki algoritma seçmesin.
    np.fill_diagonal(mesafe_matrisi_km, float('inf'))
    return mesafe_matrisi_km

def cekicilik_hesapla(mesafe_matrisi):
    """
    Görünürlük hesabı: 1 / Mesafe.
    Karıncalar kısa yolları daha çekici bulur.
    """
    cekicilik = np.zeros_like(mesafe_matrisi)
    with np.errstate(divide='ignore', invalid='ignore'):  # 0'a bölme hatalarını bastır.
        cekicilik = 1 / mesafe_matrisi
        cekicilik[mesafe_matrisi == float('inf')] = 0  # Sonsuz mesafenin çekiciliği 0'dır.
        cekicilik[mesafe_matrisi == 0] = 0  # 0 mesafenin çekiciliği 0'dır.
        cekicilik = np.nan_to_num(cekicilik)  # Olası hatalı sayıları temizle.
    return cekicilik