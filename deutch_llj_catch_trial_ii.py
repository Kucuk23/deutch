import pandas as pd
import numpy as np

# DataFrame'i oluştur
df = pd.read_csv("Deutch_Data_2022.csv", sep=";", skiprows=[1])

# Sütunları dönüştürmek için seçilen sütunlar
columns_to_convert = ['Timestamp(UTC)', 'LEG_H062_Wd', 'LEG_H062_Ws',
                      'LEG_H090_Wd', 'LEG_H090_Ws',
                      'LEG_H115_Wd', 'LEG_H115_Ws',
                      'LEG_H140_Wd', 'LEG_H140_Ws',
                      'LEG_H165_Wd', 'LEG_H165_Ws',
                      'LEG_H190_Wd', 'LEG_H190_Ws',
                      'LEG_H215_Wd', 'LEG_H215_Ws',
                      'LEG_H240_Wd', 'LEG_H240_Ws',
                      'LEG_H265_Wd', 'LEG_H265_Ws']

# Seçilen sütunları al
selected_columns = df[columns_to_convert]

# NaN değerleri içeren satırları kaldır
whole_datas = selected_columns.dropna()

# İstediğiniz başlıkların listesi
desired_columns = ['LEG_H062_Ws',
                   'LEG_H090_Ws',
                   'LEG_H115_Ws',
                   'LEG_H140_Ws',
                   'LEG_H165_Ws',
                   'LEG_H190_Ws',
                   'LEG_H215_Ws',
                   'LEG_H240_Ws',
                   'LEG_H265_Ws']

# İstediğiniz başlıklara sahip sütunları içeren bir matris oluşturun
height_datas = whole_datas[desired_columns].values

# Yeni sütunları depolamak için başlangıçta sıfırlardan oluşan bir numpy array oluşturun
llj_indic = np.zeros(len(whole_datas))
llj_level = np.zeros(len(whole_datas))

detacted_llj = []
detected_llj_date = []
detected_llj_indices = []

for m in range(len(height_datas)):
    max_indic = np.argmax(height_datas[m][1:-1]) + 1

    Min_uper_part = np.min(height_datas[m][:max_indic])
    Min_lower_part = np.min(height_datas[m][max_indic:])

    difference_lower = height_datas[m][max_indic] - Min_lower_part
    difference_upper = height_datas[m][max_indic] - Min_uper_part

    percentage_diff_upper = (difference_upper / Min_uper_part) * 100
    percentage_diff_lower = (difference_lower / Min_lower_part) * 100

    # Level 3
    if difference_lower > 4 and difference_upper > 4 and percentage_diff_upper > 40 and percentage_diff_lower > 40:  
        detacted_llj.append(height_datas[m])
        detected_llj_date.append(df.index[m])
        detected_llj_indices.append(max_indic)
        llj_indic[m] = 1
        llj_level[m] = 3
        
    # Level 2
    elif difference_lower > 3 and difference_upper > 3 and percentage_diff_upper > 30 and percentage_diff_lower > 30:
        detacted_llj.append(height_datas[m])
        detected_llj_date.append(df.index[m])
        detected_llj_indices.append(max_indic)
        llj_indic[m] = 1
        llj_level[m] = 2
        
    # Level 1
    elif difference_lower > 2 and difference_upper > 2 and percentage_diff_upper > 20 and percentage_diff_lower > 20:  
        detacted_llj.append(height_datas[m])
        detected_llj_date.append(df.index[m])
        detected_llj_indices.append(max_indic)
        llj_indic[m] = 1
        llj_level[m] = 1

# Yeni sütunları DataFrame'e ekleyin
whole_datas['llj_indic'] = llj_indic
whole_datas['llj_level'] = llj_level


# CSV dosyasına yazmak istediğiniz dosya yolunu belirtin
output_csv_path = "llj_indexed_datas.csv"

# whole_datas DataFrame'ini CSV dosyasına yazdırın
whole_datas.to_csv(output_csv_path, index=False)