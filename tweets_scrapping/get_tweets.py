import pandas as pd
import twint as tw
import nest_asyncio


def read_users(filename):
    gobernadorxs = pd.read_csv(filename)
    gobernadoras = pd.DataFrame(columns = gobernadorxs.columns)
    gobernadores = pd.DataFrame(columns = gobernadorxs.columns)

    for i in gobernadorxs.index:
        if gobernadorxs.loc[i][9]== "M":
            gobernadoras.loc[i] = gobernadorxs.loc[i]

            year,month, day = gobernadoras.loc[i][4].split('-')
            if len(year) == 2:
                year = '20'+year
            gobernadoras.loc[i][4] = year+'-'+month+'-'+day

        elif gobernadorxs.loc[i][9] == "H":
            gobernadores.loc[i] = gobernadorxs.loc[i]

            year,month,day = gobernadores.loc[i][4].split('-')
            if len(year) == 2:
                year = '20'+year
            gobernadores.loc[i][4] = year+'-'+month+'-'+day

    #Setting index correctly
    gobernadoras.index = range(len(gobernadoras))
    gobernadores.index = range(len(gobernadores))
    return gobernadoras, gobernadores

def get_replies(date_since, username):#returns DataFrame of a user
    replies = tw.Config()
    replies.Since = date_since
    replies.Pandas = True
    replies.To = username
    replies.Hide_output = True
    tw.run.Search(replies)
    df = tw.storage.panda.Tweets_df
    return df

def replies_to_file(file,filename,encoding = 'utf-8'):
    columnas = file.columns
    data = pd.DataFrame(columns=columnas)
    #data.set_index("Nombre", inplace=True)
    for i in file.index:
        print("Retrieving replies to: "+str(i))
        date_from = file.loc[i]["Fecha de inicio"]
        username = file.iloc[i][2][1:] #quitando el @
        print(username)
        data = data.append(get_replies(date_from, username))

    data.to_csv(filename, encoding=encoding)
    return data

def preprocess(df,f_out):
    missing = df[df["Usuario"].isnull() == True]
    df = df[df["Usuario"].isnull() == False]
    name = f_out[15:-4]+"_missing.csv"
    missing.to_csv("Usuarios/"+name)
    return df

def main(file_in, f_outm, f_outh):
    print("Leyendo " + file_in)
    m,h = read_users(file_in)

    print("COMENZANDO CON ELLAS")
    m_full= preprocess(m,f_outm)
    data_m = replies_to_file(m_full,f_outm)
    print("COMENZANDO CON ELLOS")
    h_full = preprocess(h,f_outm)
    data_h = replies_to_file(h_full,f_outh)


    return data_m,data_h

if __name__ == "__main__":
    file_in, f_outm, f_outh = input("Archivo Sale_m Sale_h: ").split()
    main("Usuarios/"+file_in, "Tweets/"+f_outm, "Tweets/"+f_outh)

