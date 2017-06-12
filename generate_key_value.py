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
        for index in range(1, len(data_list)):
          GENDER = data_list[index][5]
          #方法一： 如果m的下一句是f或是f的下一句是m才列為有效的對話
          #if ( index+1 < len(data_list) and data_list[index + 1][5] != GENDER ):
          #  pairs[ data_list[index][2] ] = data_list[index+1][2] 
          #  GENDER = data_list[index+1][5]
          if index + 1 < len(data_list) :
            lookahead = 1
            while  index + lookahead < len(data_list) and data_list[index + lookahead][5] == GENDER:
              lookahead += 1 
            if index + lookahead < len(data_list):
              pairs[ data_list[index][2] ] = data_list[index+lookahead][2]
    pickle.dump( pairs, open( "conversations_pairs/v2/"+filename+".p", "wb" ) )
    print (filename+ " done")

def saveToRedis():
  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  path = './conversations_pairs/v2/'
  for filename in os.listdir(path):
    data = pickle.load(open(path+filename,"rb")) 
    for key in data:
      r.set(key, data[key])
    print (filename + " done")

#generatePairs()
saveToRedis()
