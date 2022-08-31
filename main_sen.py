#Project made by Paola Gonzalez H.
#Universidad Nacional Autonoma de Mexico
#Tecnologias para la Informacion en Ciencias

import retrieve
import read_info
import pandas as pd
import twint as tw

senadoras, senadores = read_info.read_users('senadorxs.csv')
print("Starting with Senadoras")
data_gm = retrieve.replies_to_file(senadoras,"senadoras.csv")

print("Starting with Senadores")
data_gh = retrieve.replies_to_file(senadoras,"senadores.csv")