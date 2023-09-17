import pandas as pd
import os

from config import merge_desalineaciones,dump_json,get_tweets_files

tweets_mujeres = "paperspace/tweets_mujeres.csv"
tweets_hombres = "paperspace/tweets_hombres.csv"

hombres_mujeres = "paperspace/ideas mias/hombres a mujeres.csv"
mujeres_hombres = "paperspace/ideas mias/mujeres a hombres.csv"

path_ham = "Tweets_desalineaciones/hombres_a_mujeres/"
path_mah = "Tweets_desalineaciones/mujeres_a_hombres/"

df_tweets_mujeres = pd.read_csv(tweets_mujeres,usecols=["tweet"])
df_tweets_hombres = pd.read_csv(tweets_hombres,usecols=["tweet"])

desalineaciones_ham = pd.read_csv(hombres_mujeres,index_col = "word",usecols=["word","N","N1"])
desalineaciones_mah = pd.read_csv(mujeres_hombres,index_col = "word",usecols=["word","N","N1"])

print("MERGING DISALIGNMENTS N AND N1")
des_ham = merge_desalineaciones(desalineaciones_ham)
des_mah = merge_desalineaciones(desalineaciones_mah)

print("DUMPING DISALIGNMENTS TO JSON")
dump_json(des_ham, "tweets_desalineaciones/", "hombres_a_mujeres.json")
dump_json(des_mah, "tweets_desalineaciones/", "mujeres_a_hombres.json")

print("GETTING TWEETS FROM HOMBRES CORPUS")
get_tweets_files(df_tweets_hombres, des_mah, path_mah)

print("GETTING TWEETS FROM MUJERES CORPUS")
get_tweets_files(df_tweets_mujeres, des_ham, path_ham)