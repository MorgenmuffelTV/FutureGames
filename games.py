from time import sleep
import datetime as dt
import json
import mysql.connector
import igdbreq
import getToken

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="games"
)

mycursor = mydb.cursor()

def searchFromName(gameName, req):
    ret = req.searchForGame(gameName)
    #print(ret)
    if ret == -1:
        sql = "INSERT INTO UnlistedGames (Name) VALUES ('" + gameName + "')"
        mycursor.execute(sql)
        mydb.commit()
        print(mycursor.rowcount, "Unlisted record inserted. (" + gameName + ")")
        return -1
    return ret

def getIDs():
    sql = "SELECT IGDB_ID FROM Games WHERE Reload = 1 OR Timestamp > UNIX_TIMESTAMP() OR Timestamp = 0"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def getSourceIDs():
    sql = "SELECT * FROM Sources"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def getAllIDs():
    sql = "SELECT IGDB_ID FROM Games"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def searchFromID(gameID, req):
    ret = req.searchForID(gameID)
    if ret == -1:
        print ("ID: '"+gameID+"' not found, did you have a typo?")
        return(-1)
    return ret

def addsource():
    val = input("Wie soll die Source heißen?\n")
    sql = "INSERT INTO Sources (Name) VALUES ('" + val + "')"
    mycursor.execute(sql)
    mydb.commit()


def addgame(ret,update, source, or_name):
    #print(ret)   
    igdb_id = ret['id']
    name = ret['name']

    developer = ''
    publisher = ''
    if 'involved_companies' in ret:
        for j in ret['involved_companies']:
            if(j['developer'] == True):
                developer = j['company']['name']
            if(j['publisher'] == True):
                publisher = j['company']['name']

    release_hum = ''
    if 'release_dates' in ret:
        release_hum = ret['release_dates'][0]["human"]

    timestamp = 0
    if 'first_release_date' in ret:
        timestamp = ret['first_release_date']

    platforms = ''
    if 'platforms' in ret:
        string = ''
        for j in ret['platforms']:
            if string == '':
                string = string + j['name']
            else:
                string = string + ', ' + j['name']
        platforms = string

    genres = ''
    if 'genres' in ret:
        string = ''
        for j in ret['genres']:
            if string == '':
                string = string + j['name']
            else:
                string = string + ', ' + j['name']
        genres = string
    
    themes = ''
    if 'themes' in ret:
        string = ''
        for j in ret['themes']:
            if string == '':
                string = string + j['name']
            else:
                string = string + ', ' + j['name']
        themes = string

    website = ''
    buy_link = ''
    if 'websites' in ret:
        for j in ret['websites']:
            if(j['category'] == 1):
                website = j['url']
            if(j['category'] == 13):
                buy_link = j['url']
            elif(j['category'] == 16 and buy_link == ''):
                buy_link = j['url']
            elif(j['category']  == 17 and buy_link == ''):
                buy_link = j['url']
    igdb_link = ret['url']


    if update:
        sql = "UPDATE Games SET Name = %s , Developer = %s , Publisher = %s , Release_Hum = %s, Timestamp = %s , Platforms = %s, Genres = %s, Themes = %s,Website = %s, Buy_Link = %s, IGDB_Link = %s, Reload = 0 WHERE IGDB_ID = %s"
        val = (name, developer, publisher, release_hum, timestamp, platforms, genres, themes, website, buy_link, igdb_link, igdb_id)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record updated. (" + name + ")")
    else:
        sql = "INSERT INTO Games (IGDB_ID, Name, Developer, Publisher, Release_Hum, Timestamp, Platforms, Genres, Themes, Website, Buy_Link, IGDB_Link, SOURCE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (igdb_id, name, developer, publisher, release_hum, timestamp, platforms, genres, themes, website, buy_link, igdb_link, source)
        inp = input('Insert "' + name + '"? (else the original name will be inserted in unlisted) - Y or N: ')
        if inp == 'Y':
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted. (" + name + ")")
        else:
            sql = "INSERT INTO UnlistedGames (Name) VALUES ('" + or_name + "')"
            mycursor.execute(sql)
            mydb.commit()
            print(mycursor.rowcount, "Unlisted record inserted. (" + or_name + ")")


def main():
    f = open('D:\\Users\\Dennis\Repos\\Games2\\token.json','r')
    data = json.load(f)
    print(data)
    f.close()
    if dt.datetime.now() >= dt.datetime.fromisoformat(data['expire_date']):
        getToken.get_token()
    access_token = data['access_token']
    req = igdbreq.imdbRequester('ng660gwxihvlan5stt0hfln1131b3c',access_token)

    while(True):
        menu = input("Was soll gemacht werden?\n1 - Spiel hinzufügen\n2 - Aktualisieren der Daten\n3 - Aktualisieren aller Daten\n4 - Neue Source hinzufügen\n")
        if menu == '1':
            print("Welche Source soll genutzt werden?")
            for x in getSourceIDs():   
                print(str(x[0]) + ' - ' + x[1])
            inp = input()
            while(True):
                gameName = input("Welches Spiel soll hinzugefügt werden?: ")
                ret = searchFromName(gameName, req)
                if not ret == -1:
                    addgame(ret, False, inp, gameName)

        elif menu == '2':
            result = getIDs()
            for x in result:
                ret = searchFromID(x[0],req)
                addgame(ret, True, '','')
                sleep(0.25)

        elif menu == '3':
            result = getAllIDs()
            for x in result:
                ret = searchFromID(x[0],req)
                addgame(ret, True, '','')
                sleep(0.25)

        elif menu == '4':
            addsource()
    #return

if __name__ == '__main__':
    main()