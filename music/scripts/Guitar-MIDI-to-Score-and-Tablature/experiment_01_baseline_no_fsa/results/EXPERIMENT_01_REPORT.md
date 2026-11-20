# Deney 1: Kontrol Grubu Raporu (FSA Olmadan Doğrudan M2S Dönüşümü)

**Tarih:** 2026-11-20  
**Amaç:** Gitara özel perde ve tel ataması (FSA) yapılmadığında, standart açgözlü (naive greedy / en düşük perde) kuralının fiziksel zemin gerçeğine (GuitarSet JAMS) kıyasla ne kadar hata ürettiğini ölçmek.

---

## 📊 Genel Özet (Kontrol Grubu Taban Hattı)

* **Ortalama Tel Doğruluğu (String Accuracy):** **%27.9** *(Gitaristin bastığı 10 telden sadece ~2.8'i doğru!)*
* **Ortalama Perde Doğruluğu (Fret Accuracy):** **%27.9**
* **Ortalama Perde Hatası (Fret MAE):** **4.14 Perde**
* **Sol El Pozisyon Atlama Ortalaması:** **1.37 Perde** *(Gerçek Gitarist: 1.38 Perde)*

> [!WARNING]
> **Bilimsel Çıkarım:** FSA motoru kullanılmadığında naif dönüşüm **%60'ın üzerinde tel hatası** üretmektedir. Algoritma her notayı körlemesine en alt perdede (açık pozisyon) çalmaya zorladığı için, solist gitaristin 10-14. perdelerde çaldığı akıcı melodiler klavyenin dört bir yanına dağılmakta ve insan eliyle çalınamaz hale gelmektedir.

---

## 📋 Parça Bazlı Ayrıntılı Sonuçlar (Referans MIDI Girdisi)

| Parça Adı | Tür | Stil | Toplam Nota | Eşleşen | Tel Doğruluğu | Perde Doğruluğu | Perde MAE | El Kayması (Tahmin / Gerçek) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `05_BN3-119-G_solo` | Bossa Nova | Solo | 62 | 62 | **%6.5** | %6.5 | 4.5 | 1.4 / 1.3 |
| `03_Funk1-97-C_solo` | Funk | Solo | 105 | 105 | **%24.8** | %24.8 | 4.8 | 2.0 / 2.1 |
| `04_Jazz1-200-B_solo` | Jazz | Solo | 65 | 65 | **%6.2** | %6.2 | 6.1 | 1.4 / 1.6 |
| `00_Rock2-142-D_solo` | Rock | Solo | 130 | 130 | **%56.1** | %56.1 | 2.1 | 0.8 / 1.3 |
| `02_SS1-100-C#_solo` | Singer-Songwriter | Solo | 59 | 59 | **%23.7** | %23.7 | 3.6 | 1.3 / 1.5 |
| `04_BN2-131-B_comp` | Bossa Nova | Comping | 206 | 206 | **%54.9** | %54.9 | 2.1 | 0.7 / 0.9 |
| `02_Funk1-97-C_comp` | Funk | Comping | 189 | 189 | **%71.4** | %71.4 | 1.4 | 1.1 / 1.8 |
| `01_Jazz3-150-C_comp` | Jazz | Comping | 145 | 145 | **%3.5** | %3.5 | 6.9 | 1.2 / 0.8 |
| `05_Rock3-117-Bb_comp` | Rock | Comping | 398 | 398 | **%16.8** | %16.8 | 4.6 | 1.5 / 1.2 |
| `00_SS3-84-Bb_comp` | Singer-Songwriter | Comping | 184 | 184 | **%15.2** | %15.2 | 5.3 | 2.3 / 1.4 |

---

## 🎯 Sonraki Adım: Deney 2 (Açık Kaynak FSA Motorlarının Yarışması)
FSA kullanılmadığında sistemin taban hattı (%35-40 doğruluk) tescillenmiştir. Deney 2'de açık kaynak FSA motorları (`tuttut`, `gtrsnipe`, `guitar_arranger`) bu taban hattını yukarı taşımak için yarıştırılacaktır.
