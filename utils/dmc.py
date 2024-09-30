#stolen from https://github.com/sharlagelfand/dmc/tree/master 
import pandas as pd
import numpy as np

dmc_data = pd.read_csv('dmc_colors.csv')
dmc_data = dmc_data.drop('RGB code', axis=1)
dmc_data = dmc_data.drop('Row', axis=1)

table_with_colors = dmc_data.values
dmc_rgb_values = [np.array(c[2:]) for c in table_with_colors] #holds rgb values of dmc colors
dmc_labels = [np.array(c[:2]) for c in table_with_colors] #holds color names and labels

dmc_rgb_values = np.array(dmc_rgb_values).astype(float)
