import json
from pprint import pprint
import requests
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

os.chdir("/usr/local/data/www/sites/covid/")

r = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

cases = list(csv.reader(r.text.split('\n')))

df = pd.DataFrame(cases[1:], columns=cases[0])

df = df[['date', 'state', 'cases']]

df['date'] = pd.to_datetime(df['date'])
df['cases'] = pd.to_numeric(df['cases'])
# print(df.head())

df['yesterday'] = df['date'] - pd.DateOffset(1)
# print(df.head())

dfMerged = pd.merge(df, df[['date', 'state', 'cases']], how='inner', left_on=['state', 'yesterday'], right_on=['state', 'date'])
# print(dfMerged.head())

dfMerged['newCases'] = dfMerged['cases_x'] - dfMerged['cases_y']
# print(dfMerged.head())

df = dfMerged.sort_values(['state', 'date_x'])
# print(df.head())

df['avgNewCases'] = df.groupby('state')['newCases'].transform(lambda x: x.rolling(5).mean())
# print(df.head())

# df = df.sort_values(['state', 'cases_x'])



# Change the default figure size
plt.figure(figsize=(10,10))
plt.xscale("log")
plt.yscale("log")
plt.title("COVID-19 Exponentiality, top 10 states")
plt.xlabel("Total Cases")
plt.ylabel("New Cases (5 day average)")

dfMax = df.groupby('state')['cases_x'].agg({"maxpos": 'max'})
dfMax = dfMax.sort_values('maxpos', ascending=False)
states = dfMax.iloc[0:12, :].index
# print(states)

for st in states:
    plt.plot(df[df['state'] == st].cases_x, df[df['state'] == st].avgNewCases, label=st)

plt.legend(loc="upper left")
# plt.show();

plt.savefig("log_scale_figs/COVID-19 Exponetiality, top 10 states, %s.png" % dt.date.today().strftime('%Y-%m-%d'))
