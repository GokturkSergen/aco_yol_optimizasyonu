import matplotlib.pyplot as plt  # Grafik çizimi için kütüphane.
import folium  # Harita oluşturma kütüphanesi.

# ara sokaklar
def yakinsama_grafigi_ciz(en_iyi_mesafeler):
    """
    Algoritmanın her iterasyonda bulduğu en iyi mesafeleri grafiğe döker.
    """
    fig, ax = plt.subplots(figsize=(8, 4))  # 8x4 boyutunda bir grafik alanı oluştur.
    ax.plot(en_iyi_mesafeler, marker='o', linestyle='-', color='b')  # Mavi çizgili grafik çiz.
    ax.set_title("KKA İterasyon Performansı")  # Grafik başlığı.
    ax.set_xlabel("İterasyon")  # X ekseni etiketi.
    ax.set_ylabel("En Kısa Mesafe (km)")  # Y ekseni etiketi.
    ax.grid(True)  # Arka plana ızgara ekle.
    return fig  # Grafik objesini döndür.

def harita_ciz(yol, koordinatlar):
    """
    Verilen rota üzerindeki noktaları haritada işaretler ve birleştirir.
    """
    # Haritanın başlangıç merkezini, rotadaki ilk şehrin koordinatına göre ayarla.
    baslangic_noktasi = koordinatlar[yol[0]][1]
    harita = folium.Map(location=baslangic_noktasi, zoom_start=10)  # Harita objesi oluştur.

    # Rota üzerindeki koordinatları sırasıyla listeye ekle.
    rota_koordinatlari = []
    for sehir_idx in yol:
        ad, (enlem, boylam) = koordinatlar[sehir_idx]  # Şehir verisini çöz.
        rota_koordinatlari.append((enlem, boylam))  # Listeye ekle.
        
        # Haritaya kırmızı bir işaretçi (marker) ekle.
        folium.Marker(
            location=[enlem, boylam],  # Konum.
            popup=ad,  # Tıklayınca çıkan yazı.
            tooltip=ad,  # Üzerine gelince çıkan yazı.
            icon=folium.Icon(color="red", icon="info-sign")  # İkon tipi ve rengi.
        ).add_to(harita)

    # Noktaları birleştiren mavi çizgiyi (Polyline) çiz.
    folium.PolyLine(
        rota_koordinatlari,
        color="blue",  # Çizgi rengi.
        weight=2.5,    # Çizgi kalınlığı.
        opacity=1      # Görünürlük (Saydamlık yok).
    ).add_to(harita)

    return harita  # Hazırlanan harita objesini döndür.