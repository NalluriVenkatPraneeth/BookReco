#Importing Required Libraries
from flask import Flask,render_template,request
import numpy as np
import pickle
from numpy.lib.type_check import imag
import pandas as pd
import urllib.request
from PIL import Image
import Hybrid1,Hybrid2

#Initializing
app = Flask(__name__)

#Home page for the Application
@app.route('/')
def loginscreen():
    return render_template("login.html")


@app.route('/home/<pageno>',methods=["POST","GET"])
def home(pageno=1):
    userid = request.form['uname']
    psw = request.form['psw']
    dat = pd.read_csv('genre_extract.csv')
    images = dat[(int(pageno)-1)*12:int(pageno)*12]['img_l'].values
    titles = dat[(int(pageno)-1)*12:int(pageno)*12]['book_title'].values
    isbns = dat[(int(pageno)-1)*12:int(pageno)*12]['isbn'].values
    for i in range(12):
        urllib.request.urlretrieve(
            images[i],
            "static\\home\\"+str(i)+'.jpg')
        img = Image.open('static\\home\\'+str(i)+'.jpg')
        if img.size==(1,1):
            images[i]=""
    lenn = len(images)
    return render_template("review1.html",userid=userid,images=images,titles=titles,isbns=isbns,lenn=lenn,pageno=pageno)

@app.route('/search/')
@app.route('/search/<pageno>/<texttosearch>/<userid>',methods=["POST","GET"])
def search(texttosearch,pageno,userid):
    ff=""
    if int(pageno)==1:
        print(pageno)
        print(texttosearch)
        texttosearch = request.form['search']
        print(texttosearch)
    dat = pd.read_csv('genre_extract.csv')
    dat['book_title'] = dat['book_title'].str.lower()
    dat = dat[dat['book_title'].str.startswith(texttosearch)]
    images = dat[(int(pageno)-1)*12:int(pageno)*12]['img_l'].values
    titles = dat[(int(pageno)-1)*12:int(pageno)*12]['book_title'].values

    isbns = dat[(int(pageno)-1)*12:int(pageno)*12]['isbn'].values
    if len(dat)>12:
        x = 12
    else:
        x = len(dat)
    for i in range(x):
        #print(images[i])
        try:
            urllib.request.urlretrieve(
                images[i],
                "static\\"+str(i)+'.jpg')
            img = Image.open('static\\'+str(i)+'.jpg')
            if img.size==(1,1):
                images[i]=""
        except:
            print("Hello")
            ff = "No results found"
    lenn = len(images)
    return render_template("search.html",ff=ff,isbns=isbns,texttosearch=texttosearch,images=images,titles=titles,lenn=lenn,userid=userid,pageno=pageno)


@app.route('/single/<isbn>/<userid>')
def single(isbn,userid):
    r_cols = ['user_id', 'isbn', 'rating']
    ratings = pd.read_csv('BX-Book-Ratings.csv', sep=';', names=r_cols, encoding='latin-1',header=1)
    rate = ratings[ratings['isbn']==isbn]['rating'].mean()
    cont = Hybrid2.recomcont(userid,isbn)
    collab = Hybrid2.recomcollab(userid,isbn)
    print(collab)
    #collabpluscont = ['0971880107', '0316666343', '0385504209', '0060928336', '0312195516', '0142001740', '0679781587',  '0671027360', '044023722X'] 
    dat = pd.read_csv('genre_extract.csv')
    bookinfo = dat[dat['isbn']==isbn]
    urllib.request.urlretrieve(
                bookinfo['img_l'].values[0],
                "static\\single\\"+'book'+'.jpg')
    img = Image.open('static\\single\\'+'book'+'.jpg')
    if img.size==(1,1):
        imag="/static/images/not.jpg"
    else:
        imag='/static/single/book.jpg'
    recom1 = pd.DataFrame(columns=dat.columns)
    recom2 = pd.DataFrame(columns=dat.columns)
    for i in range(len(dat)):
        if dat['isbn'][i] in cont:
            recom1 = recom1.append(dat.iloc[i])
    for i in range(len(dat)):
        if dat['isbn'][i] in collab:
            recom2 = recom2.append(dat.iloc[i])
    dat1 = recom1
    dat2 = recom2
    images1 = dat1['img_l'].values
    images2 = dat2['img_l'].values
    titles1 = dat1['book_title'].values
    titles2 = dat2['book_title'].values
    alltitles1 = np.array(dat1['book_title'].values)
    alltitles2 = np.array(dat2['book_title'].values)
    isbns1 = dat1['isbn'].values
    isbns2 = dat2['isbn'].values
    for i in range(len(dat1)):
        #print(images[i])
        try:
            urllib.request.urlretrieve(
                images1[i],
                "static\\single\\content\\"+str(i)+'.jpg')
            img = Image.open('static\\single\\content\\'+str(i)+'.jpg')
            if img.size==(1,1):
                images1[i]=""
        except:
            print("Hello")
    for i in range(len(dat2)):
        #print(images[i])
        try:
            urllib.request.urlretrieve(
                images2[i],
                "static\\single\\collab\\"+str(i)+'.jpg')
            img = Image.open('static\\single\\collab\\'+str(i)+'.jpg')
            if img.size==(1,1):
                images2[i]=""
        except:
            print("Hello")
    lenn1 = len(images1)
    lenn2 = len(images2)
    titlelen1 = len(alltitles1)
    titlelen2 = len(alltitles2)
    return render_template("single.html",userid=userid,imag=imag,rate=int(rate),
    title=bookinfo['book_title'].values[0],isbn=isbn,ba=bookinfo['book_author'].values[0],yop=bookinfo['year_of_publication'].values[0],pub=bookinfo['publisher'].values[0],
    isbns1=isbns1,isbns2=isbns2,images1=images1,titles1=titles1,lenn1=lenn1,titlelen1=titlelen1,alltitles1=alltitles1,images2=images2,titles2=titles2,lenn2=lenn2,titlelen2=titlelen2,alltitles2=alltitles2)

if __name__=='__main__':
    app.run(debug=True)