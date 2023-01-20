import pandas as pd

df = pd.read_csv('sujet-1/temps_trajet30.csv', delimiter=';', encoding='latin-1')
df1 = pd.read_csv('sujet-1/niveau_interventions.csv', delimiter=';', encoding='latin-1')
df2 = pd.read_csv('sujet-1/communes_bre.csv', delimiter=';', encoding="latin-1")

merged_df = pd.merge(df, df2, left_on='destination', right_on='Nom Officiel Commune Majuscule')


merged_df_final = pd.merge(merged_df, df1, left_on='Code Officiel Commune', right_on='code_insee_commune')



