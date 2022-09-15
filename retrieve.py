#Project made by Paola Gonzalez H.
#Universidad Nacional Autonoma de Mexico
#Tecnologias para la Informacion en Ciencias

import twint as tw
import nest_asyncio
import pandas as pd
import read_info
from twint.token import RefreshTokenException

missing_files = pd.DataFrame()



def get_replies(date_since, username):#returns DataFrame of a user
    replies = tw.Config()
    replies.Since = date_since
    replies.Pandas = True
    replies.To = username
    replies.Hide_output = True
    tw.run.Search(replies)
    df = tw.storage.panda.Tweets_df
    return df

# STILL WORKING ON THIS ONE FOR STATISTICAL ANALYSIS
def get_followers(username): #returns list of followers of a username
    c = tw.Config()
    c.Username = username
    c.Pandas = True

    tw.run.Following(c)
    list_of_followings = tw.storage.panda.Follow_df

    return list_of_followings['following'][username]

def replies_to_file(file,filename,encoding = 'utf-8'):
    data = pd.DataFrame()
    missing_files = pd.DataFrame()

    for i in file.index:
        print("Retrieving replies to: "+str(file.loc[i][0]))
        date_from = file.at[i,"Fecha de inicio"]

        try :
            username = str(file.loc[i][0][1:]) #quitando el @

            data = pd.concat(data, get_replies(date_from, username))
        except TypeError:
            print("Usuario: ", str(file.loc[i][0])+ " sin usuario")
            missing_files = missing_files.append(file.loc[i][0])
            continue 
            
    data.to_csv(filename, encoding=encoding)
    return data


