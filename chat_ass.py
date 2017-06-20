# -*- coding: utf-8 -*-
from os import listdir
from gensim.models import KeyedVectors
import gensim
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import jieba.analyse
import jieba
from joblib import Parallel, delayed
import spacy
from operator import itemgetter
import redis
import random
import time
import re


class ChatAid():
  def __init__(self):
    self.r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
    self.huge_df = pd.read_csv("./all_chat_v3_cut.csv")
    self.model = KeyedVectors.load_word2vec_format("chat_w2v_v2")
    self.index = gensim.similarities.MatrixSimilarity.load('all_chat_vec_v3.index')
    print("Init Done")

  '''
  def natural_keys(text):
      alist.sort(key=natural_keys) sorts in human order
      http://nedbatchelder.com/blog/200712/human_sorting.html
      (See Toothy's implementation in the comments)
      def atoi(text):
          return int(text) if text.isdigit() else text

      return [atoi(c) for c in re.split('(\d+)', text)]
  '''

  def query2Vec(self, string):
      string_list = jieba.lcut(string)
      sent_matrix = []
      for word in string_list:
          try:
              wv = self.model[word]
              sent_matrix.append(wv)
          except:
              sent_matrix.append(np.zeros(100))
      q_vector = np.mean(np.array(sent_matrix),axis = 0)
      return(q_vector)


  def query_sent(self, q_string):
    print("Search similar words: Start")
    TIME_SEARCH = time.time()
    sims = self.index[self.query2Vec(q_string)]  #將 query餵入 index 這個 model，他算出 query 與 那些回覆 的相似度

    print("Search similar words: Done " + str(TIME_SEARCH-time.time()))
    print ("Sorting: Start")
    TIME_SORT = time.time()
    np_sort = np.argsort(sims) #照相似度排序
    print("Sorting: Done " + str(TIME_SORT-time.time()))
    sims_top = np_sort[::-1][:30] #取前五十個像的
    output_tup = []
    print("Get Conversation: Start")
    TIME_GET_CONVERSATION = time.time() 
    for sim in sims_top:
        #找到像的句子後，去找那句的下一個回覆，即是我們要推薦的
        #try:
        #key = self.huge_df.loc[sim,"text"]
        if self.huge_df.loc[sim, "sender_gender"] != self.huge_df.loc[sim+1, "sender_gender"]:  
          output_tup.append((self.huge_df.loc[sim+1, "text"], self.huge_df.loc[sim+1,"number_to_end"], self.huge_df.loc[sim, "text"]))
        #answer = self.r.get(key)
        #if (answer != None):
    print("Get Converstaion: Done " + str(TIME_GET_CONVERSATION - time.time()))

    print (sorted(output_tup , key=lambda item: -item[1])[:10])
    return sorted(output_tup , key=lambda item: -item[1])[:10]
    #return (random.sample(output_tup, 5))

if __name__ == "__main__":

  CA = ChatAid()
  while(1):
    q_string = input()
    result = CA.query_sent(q_string)
    print(result)
