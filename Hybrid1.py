import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import time
import warnings
warnings.filterwarnings('ignore')

#start_time = time.time()

def recomcont(userid,isbn):
    #Ratings
    r_cols = ['user_id', 'isbn', 'rating']
    ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', names=r_cols, encoding='latin-1',header=1)

    #Books

    items = pd.read_csv('genre_extract.csv')
    #items = items.drop(columns=['Unnamed: 0','Image-URL-S','Image-URL-M','google_id','extracted_isbn','clean_cat'])

    items['book_language'] = items['book_language'].fillna('en')
    items['categories'] = items['categories'].fillna('unknown')

    ratings = ratings[ratings['rating']!=0]
    ratings.reset_index(drop=True,inplace=True)
    rating_counts = pd.DataFrame(ratings.isbn.value_counts())
    rated_books = rating_counts[rating_counts.isbn>=5].index

    items_updated = items[items['isbn'].isin(rated_books)]
    items_updated.reset_index(drop=True,inplace=True)


    # ## Content based
    cv_cat = CountVectorizer()
    count_matrix_cat = cv_cat.fit_transform(items_updated['categories'])
    df_cat = pd.DataFrame.sparse.from_spmatrix(count_matrix_cat,columns=cv_cat.get_feature_names())

    cv_lan = CountVectorizer()
    count_matrix_lan = cv_lan.fit_transform(items_updated['book_language'])
    df_lan = pd.DataFrame.sparse.from_spmatrix(count_matrix_lan,columns=cv_lan.get_feature_names())

    cv_pub = CountVectorizer()
    count_matrix_pub = cv_pub.fit_transform(items_updated['publisher'])
    df_pub = pd.DataFrame.sparse.from_spmatrix(count_matrix_pub,columns=cv_pub.get_feature_names())

    cv_aut = CountVectorizer()
    count_matrix_aut = cv_aut.fit_transform(items_updated['book_author'])
    df_aut = pd.DataFrame.sparse.from_spmatrix(count_matrix_aut,columns=cv_aut.get_feature_names())

    cos_matrix_cat = cosine_similarity(df_cat)
    sim_cat = pd.DataFrame(cos_matrix_cat,index=items_updated['isbn'],columns=items_updated['isbn'])

    cos_matrix_lan = cosine_similarity(df_lan)
    sim_lan = pd.DataFrame(cos_matrix_lan,index=items_updated['isbn'],columns=items_updated['isbn'])

    cos_matrix_pub = cosine_similarity(df_pub)
    sim_pub = pd.DataFrame(cos_matrix_pub,index=items_updated['isbn'],columns=items_updated['isbn'])

    cos_matrix_aut = cosine_similarity(df_aut)
    sim_aut = pd.DataFrame(cos_matrix_aut,index=items_updated['isbn'],columns=items_updated['isbn'])

    result_sim = (sim_cat + sim_lan + sim_pub + sim_aut)/4

    del cv_cat,count_matrix_cat,df_cat,cos_matrix_cat,sim_cat
    del cv_lan,count_matrix_lan,df_lan,cos_matrix_lan,sim_lan
    del cv_pub,count_matrix_pub,df_pub,cos_matrix_pub,sim_pub
    del cv_aut,count_matrix_aut,df_aut,cos_matrix_aut,sim_aut
    del rated_books,rating_counts


    # **Required**
    # 
    # ISBN from page/UI --------- recom_book can change based on UI space allocation

    #from UI
    user_isbn = isbn ##########################################################################################################
    recom_df = pd.DataFrame(result_sim[user_isbn])
    recom_df = recom_df.sort_values(by=[user_isbn], ascending=False)
    recom_df = recom_df[recom_df.index!=user_isbn]
    #from UI
    recom_book = list(recom_df[:5].index)

    return recom_book
'''
# ## Collaborative filtering
userid = ratings.user_id.value_counts()[ratings.user_id.value_counts() >= 5].index
a = []
for i in range(len(ratings)):
    if ratings['user_id'][i] in userid:
        a.append(i)
u_ratings = ratings.iloc[a]
u_ratings.reset_index(drop=True,inplace=True)

useritem_matrix = pd.DataFrame(np.zeros(shape=(14220,159357),dtype=np.float16,order='F'))
useritem_matrix.columns = u_ratings['isbn'].unique()
useritem_matrix.index = sorted(u_ratings['user_id'].unique())
for i in range(len(u_ratings)):
    useritem_matrix.loc[list(u_ratings.iloc[i])[0]][list(u_ratings.iloc[i])[1]]=np.array(u_ratings.iloc[i])[2].astype('float16')
useritem_matrix.replace(0,value=np.nan, inplace = True)
row_mean = useritem_matrix.mean(axis=1)
useritem_matrix = useritem_matrix.apply(lambda x:x-row_mean.values,axis=0)
useritem_matrix.replace(np.nan,value = 0, inplace = True)
useruser_sim = cosine_similarity(useritem_matrix)
useruser_sim = pd.DataFrame(useruser_sim,index=useritem_matrix.index,columns=useritem_matrix.index)
###################################################################################################################################################
del u_ratings,useritem_matrix,row_mean


# **Required**
# 
# User-id from page/UI

user_id = userid ###################################################################################################################
sim_users = pd.DataFrame(useruser_sim[user_id])
sim_users = sim_users.sort_values(by=[user_id], ascending=False)
sim_users = sim_users[sim_users.index!=user_id]
sim_users = sim_users[sim_users[user_id]>0]
user_sim_book = list(ratings[ratings['user_id'].isin(sim_users.index)]['isbn'])
read_books = list(ratings[ratings['user_id']==user_id]['isbn'])
recom_book2 = list(set(user_sim_book).difference(read_books))


# ## Hybrid model
#from UI
final_recom_isbn = recom_book2[:5]+recom_book #######################################################################
# ## Print on UI - OUTPUT

print('Execution time : ')
print(str(time.time() - start_time) + ' seconds')'''