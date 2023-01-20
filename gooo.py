import pandas
import requests
import sklearn
import matplotlib.pyplot as plt
import os
import geopandas as gpd
import pandas as pd



df_c = pd.read_csv('data/communes_bre.csv', encoding='latin-1', sep=';')
df_n = pd.read_csv('data/niveau_interventions.csv', encoding='ansi', sep=';')
df_t = pd.read_csv('data/temps_trajet30.csv', encoding='latin-1', sep=';')

df_cs =df_c[['Nom Officiel Commune Majuscule','Code Officiel Commune']]
df_cs = df_cs.rename(columns={"Code Officiel Commune": "code_insee_commune"})

yes = pd.merge(df_n,df_cs, on='code_insee_commune')
yes2 = yes[['code_insee_commune', "Niveau d'activité réseau"]]
yes3 = yes2[yes2["Niveau d'activité réseau"] =='Très Bas']
lst = list(yes3['code_insee_commune'])

'''
url = 'https://france-geojson.gregoiredavid.fr/repo/regions/bretagne/communes-bretagne.geojson'
req = requests.get(url)
contenu = req.text
with open('data\calc.geojson','w') as output:
    output.write(contenu)
'''

calc = gpd.read_file('data/calc.geojson')
calc['code'] = calc['code'].astype(int)
south = calc[calc['code'].isin(lst)]

south.plot(ax=calc.plot(),  color="red")
