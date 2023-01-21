import pandas
import requests
import sklearn
import matplotlib.pyplot as plt
import os
import geopandas as gpd
import pandas as pd

#ouverture csv's
df_c = pd.read_csv('data/communes_bre.csv', encoding='utf-8', sep=';')
df_n = pd.read_csv('data/niveau_interventions.csv', encoding='ansi', sep=';')
df_t = pd.read_csv('data/temps_trajet30.csv', encoding='latin-1', sep=';')
df_d = pd.read_csv('data/densite.csv', encoding='latin-1', sep=';')
#Filtrage trajet inter-ville <30min 
df_t =df_t[(df_t['durée']<=1800) & (df_t['durée']!=0)]
#Fusion bases
merged_df = pd.merge(df_t, df_c, left_on='destination', right_on='Nom Officiel Commune Majuscule')
merged_df_final = pd.merge(merged_df, df_n, left_on='Code Officiel Commune', right_on='code_insee_commune')

#fonction donnat le code associé a la ville
find_code = df_c[['Code Officiel Commune','Nom Officiel Commune Majuscule']]
def ville(X):
    a = find_code[find_code['Nom Officiel Commune Majuscule']==X]['Code Officiel Commune'].values[0]
    return(a)

a = ['Très Bas','Bas']#,'Moyen']
b = ['Très Haut','Haut']#,'Moyen']
high_r_act = merged_df_final[merged_df_final["Niveau d'activité réseau"].isin(b) &
                             merged_df_final["Niveau d'activité clientèle"].isin(b)]

lst_vill_ref=[35238,22278,29019,56260,56121,35288,35115]
lst_vill_all = list(df_n['code_insee_commune'])
for i in lst_vill_ref:
    for j in merged_df_final[['code_insee_commune','depart','destination','durée']].values:
        if j[0]==i:
            try:
                lst_vill_all.remove(ville(j[1]))
            except:
                None

#importation du clac bretagne
def geojson_load():
    url = 'https://france-geojson.gregoiredavid.fr/repo/regions/bretagne/communes-bretagne.geojson'
    req = requests.get(url)
    contenu = req.text
    with open('data\calc.geojson','w') as output:
        output.write(contenu)


#tracage des cartes geopandas    
def graph_1():
    calc = gpd.read_file('data/calc.geojson')
    calc['code'] = calc['code'].astype(int)
    south = calc[calc['code'].isin(lst_vill_all)]
    south.plot(ax=calc.plot(),  color="red")
    plt.show()

def graph_2():
    calc = gpd.read_file('data/calc.geojson')
    south = df_d[['codgeo','dens_pop']]
    df = pd.merge(calc, south, left_on='code', right_on='codgeo')
    df.plot(ax=df.plot(),column ='dens_pop',  cmap="Greens")
    plt.show()

def matrice():
    df_matrice = pd.DataFrame(merged_df_final)
    df_matrice = df_matrice.explode('destination')

    matrice = pd.crosstab(df_matrice["depart"],df_matrice["destination"]).to_numpy()

    print(matrice)
    


def BFS(graph, start, end):
    # Initialisation de la file d'attente et de la liste des sommets visités
    queue = deque([start])
    visited = set()

    # Boucle de parcours
    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            if vertex == end:
                return visited
            # Ajout des voisins non visités à la file d'attente
            for neighbor in graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)

    return visited




