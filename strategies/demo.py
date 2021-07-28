from utils.get_hist_local import get_hist_data
from utils.indicators import guess_indicators

df = get_hist_data('000001')
df = guess_indicators(df)

# 'kdjk >= 80 and kdjd >= 70 and kdjj >= 100  and rsi_6 >= 80  and cci >= 100'
buy_list = df[(df['kdjk'] >= 80) & (df['kdjd'] >= 70) & (df['kdjj'] >= 100) &
              (df['rsi_6'] >= 80) & (df['cci'] >= 100)]

# kdjk <= 20 and kdjd <= 30 and kdjj <= 10  and rsi_6 <= 20  and cci <= -100
sale_list = df[(df['kdjk'] <= 20) & (df['kdjd'] <= 30) & (df['kdjj'] <= 10) &
               (df['rsi_6'] <= 20) & (df['cci'] <= -100)]

print(buy_list)
print('=' * 100)
print(sale_list)
