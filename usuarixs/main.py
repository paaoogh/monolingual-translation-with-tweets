import pandas as pd
import twint as tw
import retrieve
import read_info

mujeres, hombres = read_info.read_users('usuarios_completo.csv')

print("Starting with Mujeres")
data_m = retrieve.replies_to_file(mujeres,"Mujeres.csv")
print("Starting with Hombres")
data_h = retrieve.replies_to_file(hombres,"Hombres.csv")