#!/usr/local/bin/python3
import pandas as pd
import glob
import datetime, sys

def parse(t):
    string_ = str(t)
    try:
        return datetime.date(int(string_[:4]), int(string_[4:6]), int(string_[6:]))
    except:
        print("Erro",string_)
        return datetime.date(1900,1,1)
    
def readAllFiles():
    allFiles = glob.glob("../wta_rankings_" + "*.csv")
    ranks = pd.DataFrame()
    list_ = list()
    for filen in allFiles:
	    #print(filen)
        df = pd.read_csv(filen, 
                         index_col=None, 
                         header=None, 
                         parse_dates=[0], 
                         date_parser=None, #lambda t:parse(t),
                         low_memory=False)
        list_.append(df)
    ranks = pd.concat(list_)
    return ranks

def readPlayers():
    print ("Reading Players")
    return pd.read_csv("../wta_players.csv",
                       index_col=None,
                       header=None,                   
                       parse_dates=False,
                       encoding='ISO-8859-1')
                       
ranks = readAllFiles()
ranks = ranks[(ranks[1]<=10)]
#print ranks
players = readPlayers()
plRanks = ranks.merge(players,right_on=0,left_on=2)
print(plRanks)
#result = plRanks[['0_x','1_x','2_y','3_x']]
result = plRanks[['2_y','1_x','3_x', '0_x', '1_y', '2_y', '4_y', 5]]
result.columns = ['name','type','value','date', 'fName', 'lName', 'birth', 'country']

# S. Williams & V. Williams
result.loc[(result.fName == 'Serena') & (result.lName == 'Williams'), 'name'] = 'S. Williams'
result.loc[(result.fName == 'Venus' ) & (result.lName == 'Williams'), 'name'] = 'V. Williams'
#result.loc[(result.name == 'S. Williams'), 'lName'] = 'S. Williams'
#result.loc[(result.name == 'V. Williams'), 'lName'] = 'V. Williams'

result.value = pd.to_numeric(result.value)
print(result.dtypes)
result = result[(result.value>0)]
result = result.sort_values(by=['date', 'type'])
print(result)
result.to_csv("completeData.csv", index=False)

#write all #1 players to a file
result = result[(result.type == 1)].drop_duplicates(subset=['fName', 'lName'], keep='first')
result = result[['fName', 'lName', 'country', 'birth']]
result.to_csv("number1players.csv", index=False)
