import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Veri setlerini birleştir
llj_indexed_datas_2022 = pd.read_csv("llj_indexed_datas_2022.csv", parse_dates=["llj_indic"])
# Veri setinde llj_indic sütununda değeri 1 olan örneklerin sayısını bulma
llj_indic_1_count = (llj_indexed_datas_2022['llj_indic'] == 1).sum()

print("llj_indic sütununda değeri 1 olan örneklerin sayısı:", llj_indic_1_count)






















