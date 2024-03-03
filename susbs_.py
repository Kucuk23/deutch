

#LLJ probability Graph
"""
years = ['2018', '2019', '2020', '2021', '2022']
colors = ['r', 'g', 'b', 'c', 'm']

plt.figure(figsize=(10, 6))

for year, color in zip(years, colors):
    # CSV dosyasını oku
    df_year = pd.read_csv(f"wind_speed_df_{year}.csv")

    # Tarih sütununu indeks olarak ayarla
    df_year['Timestamp(UTC)'] = pd.to_datetime(df_year['Timestamp(UTC)'])
    df_year.set_index('Timestamp(UTC)', inplace=True)

    llj_per_month = df_year.resample('M')['LLJ'].apply(lambda x: (x == 1).sum())
    total_hours_per_month = df_year.resample('M')['LLJ'].count()
    llj_probability_per_month = (llj_per_month / total_hours_per_month) * 100

    # Ay ve LLJ olasılıklarının grafiğini çiz
    llj_probability_per_month.plot(marker='o', label=year, color=color)

plt.title('Probability of Experiencing LLJ Over Years')
plt.xlabel('Date')
plt.ylabel('Probability(%) x 100')
plt.grid(True)
plt.ylim(0, 10)  # LLJ olasılığının 0 ve 1 arasında olduğunu göstermek için
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

"""

#Wind Direction Graph
"""

def plot_wind_direction_distribution(df, height_variable_names, year):
    num_bins = 36
    
    plt.figure(figsize=(10, 8))
    plt.title(f'Wind Direction Distribution for Different Heights - {year}', fontsize=16,y=1.05)
    ax = plt.subplot(111, polar=True)
    ax.set_theta_direction(-1)  # Saat yönünde döndürme
    ax.set_theta_zero_location("N")  # Kuzeyi üst yapma
    
    # Renk listesi
    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    
    for i, height_variable_name in enumerate(height_variable_names):
        # Verilen yükseklik değişken adına sahip sütunu al
        column = df[height_variable_name]
        
        # NaN değerleri temizle ve sayısal değerlere dönüştür
        column = pd.to_numeric(column, errors='coerce').dropna()
        
        # Veriyi radyan cinsinden hesapla
        wind_direction_rad = np.deg2rad(column)
        
        # Histogramı hesapla
        wind_direction_bin_counts, _ = np.histogram(wind_direction_rad, bins=num_bins)
        
        # Polar plot
        ax.fill(np.linspace(0, 2*np.pi, num_bins), wind_direction_bin_counts, alpha=0.5, label=height_variable_name, color=colors[i])
    
    ax.legend(loc='upper right')  # Renklerin yükseklik değişkenlerine karşılık geldiğini göstermek için açıklamayı ekle
    ax.spines['polar'].set_visible(False)  # Dışardaki karenin kaldırılması
    plt.show()

# CSV dosyasını oku
df = pd.read_csv("Deutch_Data_2022.csv", sep=";")
height_variable_names = [column for column in df.columns if 'LEG' in column and '_Wd' in column]


#PLOTS
plot_wind_direction_distribution(df, height_variable_names, 2022)

"""

#LLJ Core Height Graph
"""

# LLJ değeri 0 olan örnekler için maksimum yükseklikleri al
max_heights_llj_0 = wind_speed_df.loc[wind_speed_df['LLJ'] == 0, 'Height_Max']
max_heights_llj_1 = wind_speed_df.loc[wind_speed_df['LLJ'] == 1, 'Height_Max']

min_height = min(wind_speed_df['Height_Max'])
max_height = max(wind_speed_df['Height_Max'])
num_bins = 30
bin_width = (max_height - min_height) / num_bins
bins = [min_height + i * bin_width for i in range(num_bins + 1)]

fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# LLJ=1 olanlar için histogram
axs[0].hist(max_heights_llj_1, bins=bins, color='blue', label='LLJ=1', orientation='horizontal', density=True)
axs[0].set_title('Histogram of Max Heights for LLJ')
axs[0].set_xlabel('Frequency (%)')
axs[0].set_ylabel('Max Height in Wind Profile')

# LLJ=0 olanlar için histogram
axs[1].hist(max_heights_llj_0, bins=bins, color='red', label='LLJ=0', orientation='horizontal', density=True)
axs[1].set_title('Histogram of Max Heights for No LLJ')
axs[1].set_xlabel('Frequency (%)')
axs[1].set_ylabel('Max Height in Wind Profile')

# Grafikleri göster
plt.tight_layout()
plt.show()

"""










