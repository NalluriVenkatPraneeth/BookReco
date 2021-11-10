import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import time
import warnings
warnings.filterwarnings('ignore')
import bz2
#import pickle
import _pickle as cPickle

#start_time = time.time()

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data

def recomcont(userid,isbn):
    result_sim = decompress_pickle('Finalpklcont.pbz2') 
    user_isbn = isbn ##########################################################################################################
    recom_df = pd.DataFrame(result_sim[user_isbn])
    recom_df = recom_df.sort_values(by=[user_isbn], ascending=False)
    recom_df = recom_df[recom_df.index!=user_isbn]
    #from UI
    recom_book = list(recom_df[:7].index)

    return recom_book

def recomcollab(userid,isbn):
    useruser_sim = decompress_pickle('Finalpkl.pbz2')    
    r_cols = ['user_id', 'isbn', 'rating']
    ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', names=r_cols, encoding='latin-1',header=1)    
    ratings = ratings[ratings['rating']!=0]
    ratings.reset_index(drop=True,inplace=True)
    user_id = int(userid) ###################################################################################################################
    sim_users = pd.DataFrame(useruser_sim[user_id])
    sim_users = sim_users.sort_values(by=[user_id], ascending=False)
    sim_users = sim_users[sim_users.index!=user_id]
    sim_users = sim_users[sim_users[user_id]>0]
    user_sim_book = list(ratings[ratings['user_id'].isin(sim_users.index)]['isbn'])
    read_books = list(ratings[ratings['user_id']==user_id]['isbn'])
    print(read_books)
    return read_books


    recom_book2 = list(set(user_sim_book).difference(read_books))

'''
# ## Hybrid model
#from UI
final_recom_isbn = recom_book2[:5]+recom_book #######################################################################
# ## Print on UI - OUTPUT

print('Execution time : ')
print(str(time.time() - start_time) + ' seconds')'''