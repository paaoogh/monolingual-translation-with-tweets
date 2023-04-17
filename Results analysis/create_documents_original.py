import pandas as pd
import os

from config import get_original, merge_desalineaciones

tweets_mujeres = "paperspace/tweets_mujeres.csv"
tweets_hombres = "paperspace/tweets_hombres.csv"

hombres_mujeres = "paperspace/ideas mias/hombres a mujeres.csv"
mujeres_hombres = "paperspace/ideas mias/mujeres a hombres.csv"

path_h = "Tweets_desalineaciones/originales/hombres_a_mujeres/"
path_m = "Tweets_desalineaciones/originales/mujeres_a_hombres/"

df_tweets_mujeres = pd.read_csv(tweets_mujeres,usecols=["tweet"])
df_tweets_hombres = pd.read_csv(tweets_hombres,usecols=["tweet"])

desalineaciones_ham = pd.read_csv(hombres_mujeres,index_col = "word",usecols=["word","N","N1"])
desalineaciones_mah = pd.read_csv(mujeres_hombres,index_col = "word",usecols=["word","N","N1"])

print("MERGING DISALIGNMENTS N AND N1")
des_ham = merge_desalineaciones(desalineaciones_ham)
des_mah = merge_desalineaciones(desalineaciones_mah)

try:
    os.mkdir("Tweets_desalineaciones/originales")
    os.mkdir("Tweets_desalineaciones/originales/hombres_a_mujeres")
    os.mkdir("Tweets_desalineaciones/originales/mujeres_a_hombres")
except:
    print("Directorios originales ya existen")

print("MAKE ORIGINALS FOR MUJERES")
get_original(path_m, df_tweets_mujeres, des_mah)

print("MAKE ORIGINALS FOR HOMBRES")
get_original(path_h, df_tweets_hombres, des_ham)