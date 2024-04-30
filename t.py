import pandas as pd
import numpy as np
import plotly.express as px
dataframe = pd.read_csv('merged_data.csv')
print(dataframe.head())

print(dataframe[dataframe["identityA"] == 'liberals'].describe())  
fig = px.bar(dataframe[dataframe["identityA"] == 'liberals'], x="empty_A", y="agree_A", color="agree_B", title="liberals")

fig.show()