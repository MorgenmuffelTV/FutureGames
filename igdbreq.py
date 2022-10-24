import time
import datetime as dt
import pandas as pd
import requests
import json
import sys
import os

class imdbRequester():
    def __init__(self, client_id, client_token):
        self.client_id = client_id
        self.client_token = client_token

    def getgames(self,data):
        response = requests.post("https://api.igdb.com/v4/games/",data=data,headers={"Client-ID": self.client_id,"Authorization": "Bearer "+self.client_token})
        return response.json()

    
    def searchForID(self,ID):
        ret = self.getgames('fields name, id, url, release_dates.human, first_release_date, involved_companies.company.name, involved_companies.developer, involved_companies.publisher, genres.name, themes.name, websites.*, platforms.name; where id = '+str(ID)+';')
        if len(ret) > 0:
            return ret[0]
        else: return -1

    def searchForGame(self,gameName):
        ret = self.getgames('fields name, id, url, release_dates.human, first_release_date, involved_companies.company.name, involved_companies.developer, involved_companies.publisher, genres.name, themes.name, websites.*, platforms.name; search "'+gameName+'";limit 1;')
        if len(ret) > 0:
            return ret[0]
        else: return -1


def main(file,reload):
    request = imdbRequester('ng660gwxihvlan5stt0hfln1131b3c','1ya6kxhg1e80ji0g5pyilfbeb09m4o')
    df = request.xlsxloader(file)
    #print(df)
    df = request.getGameinfoInDf(df,reload)
    print("Finnished!")
    #print(df)
    request.xlsxwriter(df,file)



if __name__ == '__main__':
    arg1 = ''
    arg2 = ''
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        if len(sys.argv) > 2:
            arg2 = sys.argv[2]
        if os.path.splitext(arg1)[1] == '.csv':
            if arg2 == 'reload':
                main(arg1,reload=True)
            else:
                main(arg1,reload=False)
        else:
            print("File must be a .csv")
    else:
        print("There must be at least [1] Argument")