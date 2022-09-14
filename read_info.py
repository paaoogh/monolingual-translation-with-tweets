#Project made by Paola Gonzalez H.
#Universidad Nacional Autonoma de Mexico
#Tecnologias para la Informacion en Ciencias

import pandas as pd

def read_users(filename):
    personas = pd.read_csv(filename)
    mujeres = pd.DataFrame(columns = personas.columns)
    hombres = pd.DataFrame(columns = personas.columns)

    for i in personas.index:
        if personas.loc[i][9]== "M":
            mujeres.loc[i] = personas.loc[i]

            day,month,year = mujeres.loc[i][4].split('-')
            if len(year) == 2:
                year = '20'+year
            mujeres.loc[i][4] = year+'-'+month+'-'+day

        elif personas.loc[i][9] == "H":
            hombres.loc[i] = personas.loc[i]

            year,month,day = hombres.loc[i][4].split('-')
            if len(year) == 2:
                year = '20'+year
            hombres.loc[i][4] = year+'-'+month+'-'+day

    #Setting index correctly
    mujeres.index = range(len(mujeres))
    hombres.index = range(len(hombres))
    return mujeres, hombres

