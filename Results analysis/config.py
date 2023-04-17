import pandas as pd
import os
import json

def merge_desalineaciones(desalineaciones):
    diccionario_desalineaciones_con_vecinos = {}
    
    for i in desalineaciones.T:
        N = desalineaciones.loc[i][0]
        N1 = desalineaciones.loc[i][1]

        lista_N = N.split("], ")
        lista_N1 = N1.split("], ")

        conjunto_vecinos = {}
        for kN,kN1 in zip(lista_N,lista_N1):
            elementoN = kN.strip("[]]").split(",")
            vecino_kN = elementoN[0][1:-1]
            distancia_N = float(elementoN[1])

            elementoN1 = kN1.strip("[]]").split(",")
            vecino_kN1 = elementoN1[0][1:-1]
            distancia_N1 = float(elementoN1[1])

            if vecino_kN not in conjunto_vecinos.keys():
                conjunto_vecinos[vecino_kN] = [distancia_N]
            elif vecino_kN in conjunto_vecinos.keys():
                conjunto_vecinos[vecino_kN].append(distancia_N)

            if vecino_kN1 not in conjunto_vecinos.keys():
                conjunto_vecinos[vecino_kN1] = [distancia_N1]
            elif vecino_kN1 in conjunto_vecinos.keys():
                conjunto_vecinos[vecino_kN1].append(distancia_N1)
        
        for k in conjunto_vecinos.keys():
            distancia_importante = sorted(conjunto_vecinos[k])[0]
            conjunto_vecinos[k] = distancia_importante
            
        diccionario_desalineaciones_con_vecinos[i] = conjunto_vecinos

    return diccionario_desalineaciones_con_vecinos


def dump_json(diccionario, path, filename):
    with open(path+filename, "w") as outfile:
        json.dump(diccionario, outfile)
    return

def get_tweets_files(tweets,des,path):
    for palabra_original in des.keys():
        os.mkdir(path+str(palabra_original)+"_original"+"/")
        print("palabra original:",palabra_original)
        lista_palabras = [palabra_original]
        diccionario_vecinos = des[palabra_original]
        
        lista_palabras = lista_palabras + list(diccionario_vecinos.keys())
        for palabra in lista_palabras:
            try:
                os.mkdir(path+str(palabra_original)+"_original"+"/"+palabra)
            except:
                print("directorio de "+ palabra + "existe")
                continue

        for desalineacion in lista_palabras: #ojo que puede que tomemos a sí misma
            print("desalineacion: ",desalineacion)
            lista_apariciones_en_tweets = []
            
            for i in tweets.T:
                tweet = str(tweets.loc[i]["tweet"])
                lista_palabras_tweet = tweet.split()
                if desalineacion in lista_palabras_tweet:
                    lista_apariciones_en_tweets.append([desalineacion,tweet])
            
            df_apariciones_en_tweets = pd.DataFrame(lista_apariciones_en_tweets,
                                                    columns = ['original', 'tweet'])
            df_apariciones_en_tweets.to_csv(path+str(palabra_original)+"_original"+"/"+str(desalineacion)+".csv")
    return


def get_original(path,df, desalineaciones):
    for des in desalineaciones.keys():
        lista_apariciones_originalmente = []
        for t in df.T:
            tweet = str(df.loc[t]["tweet"])
            lista_palabras_tweet = tweet.split()
            if des in lista_palabras_tweet or "#"+des in lista_palabras_tweet or "@"+des in lista_palabras_tweet:
                lista_apariciones_originalmente.append([des, tweet])
        df_apariciones_originales = pd.DataFrame(lista_apariciones_originalmente,
                                                    columns = ['original', 'tweet'])
        df_apariciones_originales.to_csv(path+str(des)+"_en_corpus_original.csv")

    return


def json_to_csv(file_json,path, filename):
    f = open(file_json)
    data = json.load(f)


    df = pd.DataFrame(columns = ["Palabra original",
                                 "D1", "distancia 1", 
                                 "D2", "distancia 2", 
                                 "D3", "distancia 3", 
                                 "D4", "distancia 4",
                                 "D5", "distancia 5"])
    df.set_index("Palabra original",inplace=True)
    for palabra_original in data:
        diccionario = data[palabra_original]
        lista = list(diccionario.items())
        datos = []
        for i in lista:
            datos.append(i[0])
            datos.append(i[1])

        print(palabra_original, datos)
        df.loc[palabra_original] = datos
    return df.to_csv(path+filename)