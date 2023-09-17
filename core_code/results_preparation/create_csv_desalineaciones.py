from config import json_to_csv

path_ham = "Tweets_desalineaciones/hombres_a_mujeres.json"
path_mah = "Tweets_desalineaciones/mujeres_a_hombres.json"

filename_ham = "des_ho_mu.csv"
filename_mah = "des_mu_ho.csv"

json_to_csv(path_ham,"Tweets_desalineaciones/",filename_ham)
json_to_csv(path_mah,"Tweets_desalineaciones/",filename_mah)