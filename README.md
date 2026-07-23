<p align="center">
  <img src="Resim1.png"
       alt="Küresel Yaşam Beklentisi Sınıflandırması"
       width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/pandas-Veri%20Analizi-150458?style=flat-square&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/scikit--learn-Makine%20%C3%96%C4%9Frenmesi-F7931E?style=flat-square&logo=scikitlearn&logoColor=white">
  <img src="https://img.shields.io/badge/Durum-Tamamland%C4%B1-success?style=flat-square">
  <img src="https://img.shields.io/badge/Lisans-MIT-yellow?style=flat-square">
</p>

## Araştırma Sorusu

**Mutluluk ve sosyoekonomik göstergeler kullanılarak ülkelerin yaşam beklentisi düzeyleri sınıflandırılabilir mi?**

## Kullanılan Teknolojiler

- Python
- pandas
- NumPy
- Matplotlib
- Seaborn
- scikit-learn

## Proje Hakkında

Bu projede, ülkelerin mutluluk ve sosyoekonomik göstergeleri kullanılarak yaşam beklentisi düzeylerinin sınıflandırılması amaçlanmıştır.

2015–2022 yılları arasındaki Dünya Mutluluk Raporları ile Dünya Bankası yaşam beklentisi verileri birleştirilmiştir. Veri temizleme, ülke adlarının standartlaştırılması, keşifsel veri analizi ve ön işleme adımlarının ardından farklı denetimli makine öğrenmesi algoritmaları eğitilmiş ve karşılaştırılmıştır.

Yaşam beklentisi değişkeni üç sınıfa ayrılmıştır:

- Düşük yaşam beklentisi
- Orta yaşam beklentisi
- Yüksek yaşam beklentisi

## Veri Seti

Projede iki temel veri kaynağı kullanılmıştır:

- 2015–2022 yıllarına ait Dünya Mutluluk Raporları
- Dünya Bankası yaşam beklentisi verileri

Veri setleri ülke ve yıl bilgileri kullanılarak birleştirilmiştir.

### Veri Seti Özeti

| Özellik | Değer |
|---|---:|
| Zaman aralığı | 2015–2022 |
| Ülke sayısı | 158 |
| Gözlem sayısı | 1.170 |
| Hedef sınıf sayısı | 3 |

### Kullanılan Değişkenler

| Değişken | Açıklama |
|---|---|
| Mutluluk Skoru | Ülke düzeyindeki mutluluk puanı |
| Kişi Başına GSYH | Ekonomik gelişmişlik göstergesi |
| Sosyal Destek | Algılanan sosyal destek düzeyi |
| Özgürlük | Bireylerin yaşam tercihlerini yapabilme özgürlüğü |
| Cömertlik | Ülke düzeyindeki cömertlik göstergesi |
| Yolsuzluk Algısı | Algılanan yolsuzluk düzeyi |
| Yaşam Beklentisi | Hedef sınıfların oluşturulmasında kullanılan sağlık göstergesi |

## Yaşam Beklentisi Sınıfları

| Sınıf | Tanım |
|---|---|
| Düşük | 70 yılın altı |
| Orta | 70–78 yıl arası |
| Yüksek | 78 yılın üzeri |

## Proje İş Akışı

1. Yıllık veri setlerinin toplanması
2. Ülke adlarının standartlaştırılması
3. Veri setlerinin birleştirilmesi
4. Eksik verilerin incelenmesi
5. Keşifsel veri analizi
6. IQR yöntemiyle aykırı değer analizi
7. Değişkenlerin ön işlenmesi
8. Eğitim ve test verilerinin ayrılması
9. Modellerin eğitilmesi
10. Çapraz doğrulama
11. Hiperparametre optimizasyonu
12. Model değerlendirmesi
13. Özellik önemi analizi

## Kullanılan Makine Öğrenmesi Modelleri

Aşağıdaki sınıflandırma algoritmaları değerlendirilmiştir:

- Lojistik Regresyon
- RBF çekirdekli Destek Vektör Makineleri
- Karar Ağacı
- Random Forest
- Gradient Boosting

Model performansları şu metriklerle değerlendirilmiştir:

- Test doğruluğu
- Ağırlıklı F1-skoru
- Tabakalı 10 katlı çapraz doğrulama
- Karmaşıklık matrisi

## Bulgular

Model karşılaştırması sonucunda, topluluk tabanlı ağaç yöntemlerinin diğer sınıflandırma yaklaşımlarından daha başarılı olduğu görülmüştür.

| Model | Test Doğruluğu | Ağırlıklı F1-Skoru | Ortalama Çapraz Doğrulama |
|---|---:|---:|---:|
| Lojistik Regresyon | 0.7009 | 0.7022 | 0.7282 |
| Destek Vektör Makineleri | 0.7094 | 0.7100 | 0.7479 |
| Karar Ağacı | 0.7521 | 0.7509 | 0.7726 |
| **Random Forest** | **0.8205** | **0.8215** | **0.8436** |
| Gradient Boosting | 0.7991 | 0.8005 | 0.8111 |

En yüksek genel sınıflandırma performansı Random Forest modeli ile elde edilmiştir.

Modelde en etkili değişkenler sırasıyla:

1. Mutluluk skoru
2. Kişi başına GSYH
3. Sosyal destek
4. Yolsuzluk algısı
5. Özgürlük
6. Cömertlik

olarak belirlenmiştir.

### Model Karşılaştırması

<p align="center">
  <img src="outputs/grafik_model_karsilastirma.png"
       alt="Makine öğrenmesi modellerinin karşılaştırılması"
       width="900">
</p>

### Korelasyon Matrisi

<p align="center">
  <img src="outputs/grafik_korelasyon_matrisi.png"
       alt="Korelasyon matrisi"
       width="750">
</p>

### Karmaşıklık Matrisi

<p align="center">
  <img src="outputs/grafik_confusion_matrix.png"
       alt="Random Forest karmaşıklık matrisi"
       width="650">
</p>

### Özellik Önemi

<p align="center">
  <img src="outputs/grafik_ozellik_onemi.png"
       alt="Random Forest özellik önemi"
       width="800">
</p>

## Proje Raporu

Projenin ayrıntılı raporuna aşağıdaki bağlantıdan ulaşılabilir:

[Proje raporunu görüntüle](Life_Expectancy_Analysis-Report.pdf)

## Yazar

**Hatice İkkan**

Bilgisayar Mühendisliği Yüksek Lisans Öğrencisi

- GitHub: [Haticeikkan](https://github.com/Haticeikkan)

