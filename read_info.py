#Project made by Paola Gonzalez H.
#Universidad Nacional Autonoma de Mexico
#Tecnologias para la Informacion en Ciencias

import pandas as pd

def read_users(filename):
    gobernadorxs = pd.read_csv(filename)
    gobernadoras = pd.DataFrame(columns = gobernadorxs.columns)
    gobernadores = pd.DataFrame(columns = gobernadorxs.columns)

    for i in gobernadorxs.index:
        if gobernadorxs.loc[i][9]== "M":
            gobernadoras.loc[i] = gobernadorxs.loc[i]

            day,month,year = gobernadoras.loc[i][4].split('-')
            if len(year) == 2:
                year = '20'+year
            gobernadoras.loc[i][4] = year+'-'+month+'-'+day

        elif gobernadorxs.loc[i][9] == "H":
            gobernadores.loc[i] = gobernadorxs.loc[i]

            day,month,year = gobernadores.loc[i][4].split('-')
            if len(year) == 2:
                year = '20'+year
            gobernadores.loc[i][4] = year+'-'+month+'-'+day

    #Setting index correctly
    gobernadoras.index = range(len(gobernadoras))
    gobernadores.index = range(len(gobernadores))
    return gobernadoras, gobernadores

