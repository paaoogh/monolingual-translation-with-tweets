import pandas as pd
import twint as tw
import retrieve
import read_info

gobernadoras, gobernadores = read_info.read_users('usuarios.csv')

print("Starting with Gobernadoras")
data_gm = retrieve.replies_to_file(gobernadoras,"gobernadoras_small.csv")
print("Starting with Gobernadores")
data_gh = retrieve.replies_to_file(gobernadores,"gobernadores_small.csv")