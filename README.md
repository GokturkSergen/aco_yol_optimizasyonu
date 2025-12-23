# Karınca Kolonisi Algoritması (KKA) ile Yol Optimizasyonu

Bu proje, **Karınca Kolonisi Algoritması (Ant Colony Optimization)** kullanılarak Ankara'daki 10 farklı gölet ve su kaynağı arasındaki en kısa su numunesi toplama rotasını belirlemektedir.

Proje, kuş uçuşu mesafeler yerine **Google Maps Routes API (v2)** kullanarak gerçek trafik ve yol durumuna göre en kısa sürüş rotasını hesaplar.

## 📌 Proje Konusu: Senaryo 5
**Amaç:** Çevre Bakanlığı adına Ankara'daki 10 farklı göletten (Mogan, Eymir, Mavi Göl vb.) numune toplamak için en kısa rotayı oluşturmak.

## 🚀 Özellikler
* **Gerçek Yol Verisi:** Google Routes API entegrasyonu ile gerçek sürüş mesafeleri.
* **KKA Algoritması:** Özelleştirilebilir parametrelerle (Alpha, Beta, Buharlaşma vb.) çalışan güçlü optimizasyon.
* **İnteraktif Arayüz:** Streamlit ile geliştirilmiş kullanıcı dostu web arayüzü.
* **Görselleştirme:** Folium haritası üzerinde rota çizimi ve iterasyon performans grafiği.
* **Dinamik Parametreler:** Yan menüden algoritma ayarlarını anlık değiştirme imkanı.

## 📂 Dosya Yapısı

```text
KKA_ankara/
│
├── ana_dosya.py               # Streamlit ana uygulama dosyası (Başlatmak için bunu çalıştırın)
├── ayarlar.py                 # Algoritma varsayılan parametreleri
├── requirements.txt           # Gerekli Python kütüphaneleri
├── README.md                  # Proje dökümantasyonu
│
├── core/                      # Çekirdek kodlar
│   ├── matris_araclari.py     # Google Routes API bağlantı ve matris işlemleri
│   └── karinca_algoritmasi.py # KKA matematiksel algoritması
│
├── data/                      # Veri dosyaları
│   ├── koordinatlar.py        # Ankara göletlerinin koordinat verisi
│   └── mesafe_matrisi_onbellek.csv # API çağrılarını azaltmak için önbellek dosyası
│
├── visual/                    # Görselleştirme
│   └── gorsellestirme.py      # Harita ve grafik çizim fonksiyonları
│
└── .streamlit/
    └── secrets.toml           # Google API Anahtarı (Gizli tutulur)

```

**Uygulamayı Başlatın:**
Terminalde şu komutu çalıştırın:

```bash
streamlit run main.py
```

## 📊 Parametre Açıklamaları

Uygulama arayüzünden aşağıdaki parametreleri değiştirebilirsiniz:

* **Karınca Sayısı:** Her turda yola çıkan kaşif karınca sayısı.
* **İterasyon Sayısı:** Algoritmanın kaç döngü çalışacağı.
* **Alpha (α):** Feromonun (kokunun) seçim üzerindeki etkisi. Yüksekse karıncalar popüler yolları seçer.
* **Beta (β):** Mesafenin seçim üzerindeki etkisi. Yüksekse karıncalar sadece en yakın şehre gitmeye çalışır (Açgözlü yaklaşım).
* **Buharlaşma Oranı:** Her tur sonunda yollardaki kokunun ne kadarının uçacağını belirler.

## ⚠️ Önemli Notlar

* **API Güvenliği:** `secrets.toml` dosyası `.gitignore` dosyasına eklenmiştir ve GitHub'a yüklenmez.
* **Önbellek (Cache):** Google API kotasını harcamamak için çekilen mesafeler `data/` klasörüne CSV olarak kaydedilir.

## 👤 Öğrenci Bilgileri

* **Adı Soyadı:** Sergen Göktürk
* **Okul Numarası:** 2212721075
* **Repo Bağlantısı:** https://github.com/GokturkSergen/aco_yol_optimizasyonu/
