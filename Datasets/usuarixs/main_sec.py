#Project made by Paola Gonzalez H.
#Universidad Nacional Autonoma de Mexico
#Tecnologias para la Informacion en Ciencias

import retrieve
import read_info
import pandas as pd
import twint as tw

secretarias, secretarios = read_info.read_users('secretarixs_ejec.csv')
print("Starting with Secretarias")
data_gm = retrieve.replies_to_file(secretarias,"secretarias.csv")

print("Starting with Secretrarios")
data_gh = retrieve.replies_to_file(secretarios,"secretarios.csv")

