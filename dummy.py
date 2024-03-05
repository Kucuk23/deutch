import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable

# Veri setlerini birleştir
llj_indexed_datas_2022 = pd.read_csv("llj_indexed_datas_2022.csv", parse_dates=["Timestamp(UTC)"])

# Mevsimler için ay aralıklarını tanımla
seasons = {
    'Winter': [12, 1, 2],  # Aralık, Ocak, Şubat
    'Spring': [3, 4, 5],    # Mart, Nisan, Mayıs
    'Summer': [6, 7, 8],    # Haziran, Temmuz, Ağustos
    'Autumn': [9, 10, 11]   # Eylül, Ekim, Kasım
}

# Tek bir figür oluştur
fig, axs = plt.subplots(1, 4, figsize=(16, 6), subplot_kw=dict(polar=True))
R = 30

# Renk skalası için altta bir axe oluştur
cax = fig.add_axes([0.92, 0.1, 0.02, 0.8])

# Her mevsim için döngü
for ax, (season, months) in zip(axs, seasons.items()):
    # Sezon için ay listesini filtrele ve sadece LLJ 1 verilerini seç
    season_data = llj_indexed_datas_2022[(llj_indexed_datas_2022['Timestamp(UTC)'].dt.month.isin(months)) &
                                          (llj_indexed_datas_2022['llj_indic'] == 1)]
    llj_indic_1_count = (llj_indexed_datas_2022['llj_indic'] == 1).sum()

    # Rüzgar yönlerini ve hızlarını al
    angles = season_data['LEG_H090_Wd']
    velocities = season_data['LEG_H090_Ws']

    # Rüzgar yönlerini binslere böl
    wind_direction_bins = np.linspace(0, 360, num=19)  # 0 ile 360 derece arası 36 eşit parçaya bölünmüş bins
    hist, bins = np.histogram(angles, bins=wind_direction_bins)

    # Her mevsim için ayrı subplot oluştur
    ax.set_theta_direction(-1)  # Saat yönünde açıların artması için
    ax.set_theta_zero_location('N')  # Kuzey yönünü sıfır olarak ayarla
    ax.set_title(f' Histogram of Wind Direction - {season}         ', fontsize=8, fontweight='bold', y=1.1)

    # Yönleri temsil eden kısaltmaları ve doğru yönlerin koordinatlarını ekle
    ax.text(np.deg2rad(0), R + 1, 'N', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.text(np.deg2rad(90), R + 1, 'E', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.text(np.deg2rad(180), R + 3, 'S', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.text(np.deg2rad(270), R + 2, 'W', ha='center', va='bottom', fontsize=8, fontweight='bold')

    # X ekseni etiketlerini kapat
    ax.set_xticklabels([])

    # Çizgi çizmek için açıyı belirleyin (örneğin 45 derece)
    angle_rad = np.deg2rad(40)
    angle_rad2 = np.deg2rad(220)
    # Çizgi başlangıç ve bitiş noktalarını belirleyin
    line_start = (0, 0)
    line_end = (angle_rad, R)
    line_end_2 = (angle_rad2, R)
    # Çizgiyi çizin
    ax.plot([line_start[0], line_end[0]], [line_start[1], line_end[1]], color='green', linewidth=5, label='SHORE')
    ax.plot([line_start[0], line_end_2[0]], [line_start[1], line_end_2[1]], color='green', linewidth=5)

    # Grafiklerin boyutunu ayarla
    ax.set_ylim(0, R)  # Y ekseni aralığını istediğiniz gibi ayarlayabilirsiniz
    ax.set_xlim(0, 2*np.pi)  # X ekseni aralığını 0'dan 2*pi'ye ayarlar, yani tam bir daire olur.

    # Belirli bir açı aralığı için arka plan rengini ayarla
    start_angle = 45
    end_angle = 135

    # Her bir çubuğun renk bölümlerini hesapla ve ekle
    for i in range(len(bins) - 1):
        start_angle = bins[i]
        end_angle = bins[i + 1]
        # Belirli bir açı aralığındaki hızları al
        velocities_in_bin = velocities[(angles >= start_angle) & (angles < end_angle)]
        # Ortalama hızı hesapla
        mean_velocity = velocities_in_bin.mean()
        # Renk kodunu hesapla (örneğin, hızın yüzdeye göre mavi tonu)
        color = plt.cm.Blues(mean_velocity / velocities.max())
        # Çubuğun renkli bölümünü ekle
        ax.bar([np.deg2rad(start_angle), np.deg2rad(end_angle)], [hist[i], hist[i]], width=np.deg2rad(360/18),
               color=color, edgecolor='black')

# Renk skalasını legend'a ekle
sm = ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(vmin=velocities.min(), vmax=velocities.max()))
sm.set_array([])
cbar = plt.colorbar(sm, cax=cax, fraction=0.01)
cbar.set_label('Velocity')

# Grafikleri göster
plt.suptitle('Histogram of 2022 Wind Direction @90m for Different Seasons when LLJ=1', fontsize=12, fontweight='bold', y=0.9)
plt.tight_layout(rect=[0.1, 0.1, 0.9, 0.9])
plt.show()
