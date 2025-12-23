import numpy as np  # Matematik kütüphanesi.
import random  # Rastgele sayı üretimi için.
from core.matris_araclari import cekicilik_hesapla  # Çekicilik hesaplayan fonksiyonu çağır.

def olasilik_hesapla(mevcut_konum, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta):
    """
    Bir sonraki şehre gitme olasılığını hesaplar.
    Formül: (Feromon ^ alpha) * (Çekicilik ^ beta)
    """
    toplam_olasilik = 0
    olasiliklar = {}
    
    for hedef in ziyaret_edilmemisler:
        # Formülü uygula
        f_degeri = feromon[mevcut_konum][hedef]
        c_degeri = cekicilik[mevcut_konum][hedef]
        
        deger = (f_degeri ** alpha) * (c_degeri ** beta)
        olasiliklar[hedef] = deger
        toplam_olasilik += deger
        
    # Olasılıkları normalize et (Toplamları 1 olacak şekilde böl).
    for hedef in olasiliklar:
        if toplam_olasilik > 0:
            olasiliklar[hedef] /= toplam_olasilik
        else:
            # Eğer toplam 0 ise (feromon yoksa) rastgele şans ver.
            olasiliklar[hedef] = 1.0 / len(ziyaret_edilmemisler)
            
    return olasiliklar

def rulet_tekerlegi_secimi(olasilik_dict):
    """
    Hesaplanan olasılıklara göre rastgele bir şehir seçer.
    
    """
    sans = random.random()  # 0 ile 1 arası sayı tut.
    toplam = 0
    for sehir, olasilik in olasilik_dict.items():
        toplam += olasilik
        if sans <= toplam:  # Kümülatif toplama denk gelirse seç.
            return sehir
    return list(olasilik_dict.keys())[-1]  # Hata durumunda sonuncuyu dön.

def karinca_turu(baslangic, mesafe, feromon, alpha, beta):
    """
    Tek bir karıncanın tüm şehirleri gezdiği fonksiyon.
    """
    n = len(mesafe)
    yol = [baslangic]  # Başlangıç şehrini yola ekle.
    toplam_uzunluk = 0
    cekicilik = cekicilik_hesapla(mesafe)  # Mesafeye göre çekicilik matrisi.
    
    # Tüm şehirler gezilene kadar döngü kur.
    while len(yol) < n:
        mevcut = yol[-1]  # Şu anki konum.
        # Ziyaret edilmemiş şehirleri bul.
        ziyaret_edilmemisler = list(set(range(n)) - set(yol))
        
        # Olasılıkları hesapla ve bir sonraki şehri seç.
        olasiliklar = olasilik_hesapla(mevcut, ziyaret_edilmemisler, feromon, cekicilik, alpha, beta)
        secilen = rulet_tekerlegi_secimi(olasiliklar)
        
        yol.append(secilen)  # Seçileni yola ekle.
        toplam_uzunluk += mesafe[mevcut][secilen]  # Mesafeyi topla.
    
    # Son şehirden başlangıça geri dön (Tur tamamla).
    toplam_uzunluk += mesafe[yol[-1]][yol[0]]
    yol.append(yol[0])
    
    return yol, toplam_uzunluk

def feromon_guncelle(feromon, yollar, buharlasma_orani, Q):
    """
    Tur sonunda yollardaki kokuları günceller.
    """
    # 1. Buharlaşma: Mevcut feromonları belirli oranda azalt.
    yeni_feromon = (1 - buharlasma_orani) * feromon
    
    # 2. Yeni Feromon Ekleme: Karıncaların geçtiği yollara koku ekle.
    for yol, uzunluk in yollar:
        if uzunluk < 1e-9: uzunluk = 1e-9  # 0'a bölme hatası önlemi.
            
        for i in range(len(yol) - 1):
            a, b = yol[i], yol[i + 1]
            katki = Q / uzunluk  # Yol ne kadar kısaysa o kadar çok koku bırak.
            yeni_feromon[a][b] += katki
            yeni_feromon[b][a] += katki  # Yol gidiş-dönüş aynıdır.
            
    return yeni_feromon

def kka_calistir(mesafe_matrisi, karinca_sayisi, iterasyon_sayisi, alpha, beta, buharlasma_orani, feromon_katkisi):
    """
    Ana KKA Döngüsü.
    """
    # Mesafe matrisi boş veya sıfırsa işlem yapma.
    if np.sum(mesafe_matrisi) == 0:
        return list(range(len(mesafe_matrisi))), 0, [0]*iterasyon_sayisi

    # Başlangıç feromon seviyesi (rastgele küçük değerler).
    feromon = np.ones_like(mesafe_matrisi) * 0.1
    
    en_iyi_yol = None
    en_kisa_mesafe = float("inf")  # Başlangıçta sonsuz kabul et.
    iterasyon_gecmisi = []  # Grafik çizimi için geçmişi tut.
    
    # Belirtilen iterasyon sayısı kadar döngü kur.
    for it in range(iterasyon_sayisi):
        yollar = []
        
        # Her iterasyonda karıncaları yola çıkar.
        for _ in range(karinca_sayisi):
            baslangic_sehri = random.randint(0, len(mesafe_matrisi)-1)
            yol, uzunluk = karinca_turu(baslangic_sehri, mesafe_matrisi, feromon, alpha, beta)
            yollar.append((yol, uzunluk))
            
            # Eğer bulunan yol şimdiye kadarki en iyisiyse kaydet.
            if uzunluk < en_kisa_mesafe:
                en_kisa_mesafe = uzunluk
                en_iyi_yol = yol
        
        # Tüm karıncalar turu bitirince feromonları güncelle.
        feromon = feromon_guncelle(feromon, yollar, buharlasma_orani, feromon_katkisi)
        iterasyon_gecmisi.append(en_kisa_mesafe)
        
    return en_iyi_yol, en_kisa_mesafe, iterasyon_gecmisi