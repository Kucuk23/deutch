import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Veri setlerini birleştir
merged_data = pd.read_csv("Deutch_Data_2022.csv", sep=";", skiprows=[1])


# Veri setindeki tarih sütununu datetime formatına dönüştür
merged_data['Date'] = pd.to_datetime(merged_data['Timestamp(UTC)'])

# Mevsimler için ay aralıklarını tanımla
seasons = {
    'Winter': [12, 1, 2],  # Aralık, Ocak, Şubat
    'Spring': [3, 4, 5],    # Mart, Nisan, Mayıs
    'Summer': [6, 7, 8],    # Haziran, Temmuz, Ağustos
    'Autumn': [9, 10, 11]   # Eylül, Ekim, Kasım
}

# Tek bir figür oluştur
fig, axs = plt.subplots(1, 4, figsize=(12, 4), subplot_kw=dict(polar=True))

# Her mevsim için döngü
for ax, (season, months) in zip(axs, seasons.items()):
    # Sezon için ay listesini filtrele ve sadece LLJ 1 verilerini seç
    season_data = merged_data[(merged_data['Date'].dt.month.isin(months)) & (merged_data['LLJ'] == 0)]
    
    # Rüzgar yönlerini al
    angles = season_data['Wind_Direction_(deg)_at_38m']

    # Rüzgar yönlerini binslere böl
    wind_direction_bins = np.linspace(0, 360, num=19)  # 0 ile 360 derece arası 36 eşit parçaya bölünmüş bins
    hist, bins = np.histogram(angles, bins=wind_direction_bins)

    # Her mevsim için ayrı subplot oluştur
    ax.bar(np.deg2rad(bins[:-1]), hist, width=np.deg2rad(360/18), color='gray', edgecolor='black')
    ax.set_theta_direction(-1)  # Saat yönünde açıların artması için
    ax.set_theta_zero_location('N')  # Kuzey yönünü sıfır olarak ayarla
    ax.set_title(f'Circular Histogram of Wind Direction - {season}', fontsize=6, fontweight='bold', y=1.1)

    # Güneybatı yönünde kalın bir çizgi çiz
    ax.plot(np.deg2rad([225, 225]), [0, max(hist)], color='green', linewidth=3, label='Shore Direction')
    ax.legend(loc='lower right', fontsize=6)

    # Yönleri temsil eden kısaltmaları ve doğru yönlerin koordinatlarını ekle
    ax.text(np.deg2rad(0), max(hist) + 5, 'N', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.text(np.deg2rad(90), max(hist) + 5, 'E', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.text(np.deg2rad(180), max(hist) + 5, 'S', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.text(np.deg2rad(270), max(hist) + 5, 'W', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # X ekseni etiketlerini kapat
    ax.set_xticklabels([])

# Grafikleri göster
plt.suptitle('Histogram of Wind Direction for Different Seasons when LLJ=0', fontsize=10, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0.1, 0.1, 0.9, 0.9])
plt.show()
