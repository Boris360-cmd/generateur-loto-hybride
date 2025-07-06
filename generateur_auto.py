import pandas as pd
import random
from numpy.random import choice
from collections import defaultdict
from datetime import datetime
import os
import glob

def charger_tirages_realistes():
    csv_files = glob.glob("data/*.csv")
    dataframes = []
    for file in csv_files:
        try:
            df = pd.read_csv(file, sep=';', encoding='utf-8')
            dataframes.append(df)
        except:
            pass
    if not dataframes:
        return []
    df_all = pd.concat(dataframes, ignore_index=True)
    if "1er_ou_2eme_tirage" in df_all.columns:
        df_filtered = df_all[(df_all["1er_ou_2eme_tirage"].isna()) | (df_all["1er_ou_2eme_tirage"] != "2")]
    else:
        df_filtered = df_all.copy()
    colonnes_boules = ['boule_1', 'boule_2', 'boule_3', 'boule_4', 'boule_5']
    df_filtered = df_filtered[colonnes_boules].dropna().astype(int)
    return [list(row) for row in df_filtered.itertuples(index=False, name=None)]

def creer_frequences(historique):
    plages = {
        '1–10': defaultdict(int),
        '11–20': defaultdict(int),
        '21–30': defaultdict(int),
        '31–40': defaultdict(int),
        '41–49': defaultdict(int),
    }

    def plage(num):
        if 1 <= num <= 10: return '1–10'
        elif 11 <= num <= 20: return '11–20'
        elif 21 <= num <= 30: return '21–30'
        elif 31 <= num <= 40: return '31–40'
        else: return '41–49'

    for comb in historique:
        for num in comb:
            plages[plage(num)][num] += 1

    dfs = {label: pd.DataFrame(sorted(freq.items()), columns=["Numéro", "Fréquence"])
           for label, freq in plages.items()}
    total = {k: df["Fréquence"].sum() for k, df in dfs.items()}
    classement = sorted(total.items(), key=lambda x: x[1], reverse=True)
    return {f"Plage {i+1}": dfs[label] for i, (label, _) in enumerate(classement)}

def generer_grille(df_par_plage):
    grille = []
    for plage in ["Plage 3", "Plage 4", "Plage 2", "Plage 5"]:
        df = df_par_plage[plage]
        num = choice(df["Numéro"], p=df["Fréquence"] / df["Fréquence"].sum())
        grille.append(num)
    num_alea = random.choice(df_par_plage["Plage 1"]["Numéro"])
    grille.append(num_alea)
    return sorted(grille)

def main():
    historique = charger_tirages_realistes()
    if not historique:
        print("Erreur : aucun fichier de tirages valide.")
        return
    plages = creer_frequences(historique)
    grilles = [generer_grille(plages) for _ in range(4)]
    df_resultats = pd.DataFrame({
        "Grille #": [f"Grille {i+1}" for i in range(4)],
        "Numéros": grilles
    })
    now = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("grilles", exist_ok=True)
    df_resultats.to_csv(f"grilles/grilles_{now}.csv", index=False)
    print(f"✅ Grilles générées dans grilles/grilles_{now}.csv")

if __name__ == "__main__":
    main()
# Script auto – contenu à coller depuis l'éditeur
