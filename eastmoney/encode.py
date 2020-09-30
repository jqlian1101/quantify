#-*-coding: utf-8 -*-

import numpy as np
import pandas as pd


data = pd.read_csv('./files/history/000002.csv', encoding = 'gb2312', index_col = 0)

print(data)


