import os
import csv
import sys
import pickle
import redis
csv.field_size_limit(sys.maxsize)
path = './preprocessing_45_900/'

def generatePairs():
  for filename in os.listdir(path):
    with open (path+filename) as csvFile:
      pairs = {}
      reader = csv.reader(csvFile)
      data_list = list(reader)
      if (len(data_list) > 1):
        GENDER = data_list[1][5]
        for index in range(1, len(data_list)):
          if ( index+1 < len(data_list) and data_list[index + 1][5] != GENDER ):
            pairs[ data_list[index][2] ] = data_list[index+1][2] 
            GENDER = data_list[index+1][5]
    pickle.dump( pairs, open( "conversations_pairs/"+filename+".p", "wb" ) )

  print("DONE")

def saveToRedis():
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  path = './conversations_pairs/'
  for filename in os.listdir(path):
    data = pickle.load(open(path+filename,"rb")) 
    for key in data:
      print (data[key])
      r.set(key, data[key])

saveToRedis()
