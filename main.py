from flask import Flask,redirect,url_for,render_template,request
from pprint import pprint
from datetime import datetime
from time import strftime,gmtime
import json
import time
import pandas as pd
from pandas import Timestamp
from collections import Counter

app=Flask(__name__)
@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        if request.form["redirection"]=="Chercher par semaine" :
           return redirect("/semaine")
        if request.form["redirection"]=="Toutes les frquences" :  
           return redirect("/freq")
    return render_template("home.html")
@app.route("/semaine",methods=["POST","GET"])
def semaine():
    l=[]
    c="this"
    index=0
    f=0
    semaine=""
    freq=[]
    with open("C:\\Users\\asus\\Downloads\\jeu_journaux\\journaux.json", encoding="utf8") as f:
      data = json.load(f)
    for a in data['articles']:
      a['published']= datetime.strptime(a['published'],"%Y-%m-%dT%H:%M:%S.%f%z")  
    df=pd.DataFrame(data['articles'], columns=['type', 'title', '@timestamp','published'])
    ##decouper en semaine : 
    weeks = [g.reset_index() for n, g in df.groupby(pd.Grouper(key='published',freq='W'))]
    
    if request.method=="POST":

      semaine=request.form["week"]
      semaine=semaine[6]+semaine[7]
      semaine=int(semaine)     
      ## compter les mots les plus fréquents
      for f,i in enumerate(weeks) :
          d=weeks[f]['published'][0].strftime('%m/%d/%y')
          s = time.strptime(d,"%m/%d/%y")
          if int(strftime( '%U',s))==semaine:
              index=f   
      freq=Counter(" ".join(weeks[index]["title"]).split()).most_common(10)
      #creer un fichier json pour toutes les semaines avec les mots les plus fréquents 

    f=0
    for i in weeks :
      #l.append([time.strptime(weeks[f]["published"][0].strftime('%m/%d/%y'),"%m/%d/%y"),Counter(" ".join(i["title"]).split()).most_common(10)])
      l.append([strftime('Semaine:%U-%Y',time.strptime(weeks[f]["published"][0].strftime('%m/%d/%y'),"%m/%d/%y")),Counter(" ".join(i["title"]).split()).most_common(10)])

      f=f+1
    #mettrer la structure dans un dataframe
    df1= pd.DataFrame(l)
    #importer dans un fichier json
    js = df1.to_json(orient = 'records')
    with open('structure.json', 'w') as f:
      f.write(js)    
    return render_template("index.html",content=freq,data=l) 

@app.route("/<name>")    
def user(name):
    return f"hello {name}"
@app.route("/freq",methods=["POST","GET"])
def freq():
    l=[]
   
    f=0
    semaine=""
    freq=[]
 
    with open("C:\\Users\\asus\\Downloads\\jeu_journaux\\journaux.json", encoding="utf8") as f:
      data = json.load(f)
    for a in data['articles']:
      a['published']= datetime.strptime(a['published'],"%Y-%m-%dT%H:%M:%S.%f%z")  
    df=pd.DataFrame(data['articles'], columns=['type', 'title', '@timestamp','published'])
    ##decouper en semaine : 
    weeks = [g.reset_index() for n, g in df.groupby(pd.Grouper(key='published',freq='W'))]
    f=0
    for i in weeks :
      #l.append([time.strptime(weeks[f]["published"][0].strftime('%m/%d/%y'),"%m/%d/%y"),Counter(" ".join(i["title"]).split()).most_common(10)])
      l.append([strftime('Semaine:%U-%Y',time.strptime(weeks[f]["published"][0].strftime('%m/%d/%y'),"%m/%d/%y")),Counter(" ".join(i["title"]).split()).most_common(10)])

      f=f+1
    #mettrer la structure dans un dataframe
    df1= pd.DataFrame(l)
    #importer dans un fichier json
    js = df1.to_json(orient = 'records')
    with open('structure.json', 'w') as f:
      f.write(js)    
    return render_template("weekly.html",data=l) 
if __name__=="__main__":
   app.run()