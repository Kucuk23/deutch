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

columns_to_convert_velocities = ['LEG_H062_Ws',
                      'LEG_H090_Ws',
                      'LEG_H115_Ws',
                      'LEG_H140_Ws',
                      'LEG_H165_Ws',
                      'LEG_H190_Ws',
                      'LEG_H215_Ws',
                      'LEG_H240_Ws',
                      'LEG_H265_Ws']

# Seçilen sütunları al
selected_columns = df[columns_to_convert]

# Daha sonra, istediğiniz sütunları NumPy dizisine ekleyin
llj_indic = np.zeros(len(selected_columns))
llj_level = np.zeros(len(selected_columns))
max_indic = np.zeros(len(selected_columns))
time_date= np.zeros(len(selected_columns))

detacted_llj = []
detected_llj_date = []
detected_llj_indices = []
flag = []


counter_NAN = 0
llj_counter = 0

height_columns = [col for col in selected_columns.columns if 'LEG_H' in col and col.endswith('_Ws')]
heights = [col.split('_')[1] for col in height_columns]
height_vectors = selected_columns[columns_to_convert_velocities].values

# NaN değerleri içeren satırları kaldır
nan_indices = np.any(np.isnan(height_vectors), axis=1)
height_vectors = height_vectors[~nan_indices]


for m in range(len(height_vectors)):
    max_indic[m] = np.argmax(height_vectors[m][1:-1]) + 1

    max_indices_=int(max_indic[0])

    Min_uper_part = np.min(height_vectors[m][:max_indices_])
    Min_lower_part = np.min(height_vectors[m][max_indices_:])

    difference_lower = height_vectors[m][max_indices_] - Min_lower_part
    difference_upper = height_vectors[m][max_indices_] - Min_uper_part

    percentage_diff_upper = (difference_upper / Min_uper_part) * 100
    percentage_diff_lower = (difference_lower / Min_lower_part) * 100

    llj_indic = 0
    llj_level = 0
    
    # Level 3
    if difference_lower > 4 and difference_upper > 4 and percentage_diff_upper > 40 and percentage_diff_lower > 40:  
        detacted_llj.append(height_vectors[m])
        detected_llj_date.append(df.index[m])
        detected_llj_indices.append(max_indices_)
        llj_indic = 1
        llj_level = 3
        
    # Level 2
    elif difference_lower > 3 and difference_upper > 3 and percentage_diff_upper > 30 and percentage_diff_lower > 30:
        detacted_llj.append(height_vectors[m])
        detected_llj_date.append(df.index[m])
        detected_llj_indices.append(max_indices_)
        llj_indic = 1
        llj_level = 2
        
    # Level 1
    elif difference_lower > 2 and difference_upper > 2 and percentage_diff_upper > 20 and percentage_diff_lower > 20:  
        detacted_llj.append(height_vectors[m])
        detected_llj_date.append(df.index[m])
        detected_llj_indices.append(max_indices_)
        llj_indic = 1
        llj_level = 1
        
    
    height_vectors[m, -3] = llj_indic
    height_vectors[m, -2] = llj_level
    height_vectors[m, -1] = max_indices_



