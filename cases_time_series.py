import json
from pprint import pprint
import requests
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import csv

r = requests.get('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')

cases = list(csv.reader(r.text.split('\n')))

df = pd.DataFrame(cases[1:], columns=cases[0])

df = df[['date', 'state', 'cases']]

df['date'] = pd.to_datetime(df['date'])
df['cases'] = pd.to_numeric(df['cases'])
# print(df.head())

# filter to only cases > 10
df = df[df['cases'] >= 10]

dfTenthCase = df.groupby('state').agg({'date': "min"})
dfTenthCase = dfTenthCase.rename(columns={"date": "dtFirst"})

dfTime = pd.merge(df, dfTenthCase, on="state")
dfTime['dsfc'] = dfTime.apply(lambda x: (x.date - x.dtFirst).days, axis=1)
print(dfTime.head())

plt.figure(figsize=(10,10))
plt.title("COVID-19 Cases over Time")
plt.ylabel("Total Cases")
plt.xlabel("Days since 10th case")

dfMax = df.groupby('state')['cases'].agg({"maxpos": 'max'})
dfMax = dfMax.sort_values('maxpos', ascending=False)
states = dfMax.iloc[0:12, :].index

for st in states:
    plt.plot(dfTime[dfTime['state'] == st].dsfc, dfTime[dfTime['state'] == st].cases, label=st)

plt.legend(loc="upper left")

plt.savefig("time_series_figs/COVID-19 Cases over time, %s.png" % dt.date.today().strftime('%Y-%m-%d'))
