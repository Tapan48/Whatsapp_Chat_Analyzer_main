from urlextract import URLExtract
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
extractor = URLExtract()

def fetch_stats(user,df):
    
    if user=="Overall":
        
        no_media_msgs=df[df["Message"]=="<Media omitted>"].shape[0]
        links=[]

        for message in df["Message"]:
            links.extend(extractor.find_urls(message))
        
        words = []
        for i, row in df.iterrows():
            if row["User"] != "group notification":
                message_words = row["Message"].split()
                words.extend(message_words)
                
        df=df[df["User"]!="group notification"]     
        
        return df.shape[0],len(words),no_media_msgs,len(links)
    else:
        
        newdf=df[df["User"]==user]
    
        user_noof_msgs=newdf.shape[0]
        
        
        no_media_msgs=newdf[newdf["Message"]=="<Media omitted>"].shape[0]
        links=[]
        
        for message in newdf["Message"]:
            links.extend(extractor.find_urls(message))
        
       
        words = []
        for i, row in newdf.iterrows():
            
                message_words = row["Message"].split()
                words.extend(message_words)
        return user_noof_msgs,len(words),no_media_msgs,len(links)
   
   
def most_busy_users(df):
    
    df1=df["User"].value_counts().head()
    
    newdf=round((df["User"].value_counts()/df.shape[0])*100,2).reset_index()
    newdf=newdf.rename(columns={"index":"User","User":"percent(%)"})
    
    return df1,newdf   #### df1 contains data of top 5 users and their  messages_count,  newdf consists of users and their percentage of messages        
    
def word_cloud(user,df):
    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    
    temp=df[df["User"]!="group notification"]
    final_df=temp[temp["Message"]!="<Media omitted>"]
    
    
    def remove_stopwords(message):
    
        words=[]

                  ###### remove stop words
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word) 
        return " ".join(words)        
                    
                    
    
    if user=="Overall":
        
        
        
        final_df["Message"]=final_df["Message"].apply(remove_stopwords)

        # Create a WordCloud object with the desired parameters
        wc = WordCloud(width=800, height=800,min_font_size=10, background_color='white')
        df_wc =wc.generate(final_df['Message'].str.cat(sep=" "))
        
        
        
    
    else:
        newdf=final_df[final_df["User"]==user]
        newdf["Message"]=newdf["Message"].apply(remove_stopwords)
   
        

        # Create a WordCloud object with the desired parameters
        wc = WordCloud(width=800, height=800, min_font_size=10, background_color='white')
        df_wc=wc.generate(newdf['Message'].str.cat(sep=" "))
    
    return df_wc    
     
        
            
def top_20_most_words(df,user):
    temp=df[df["User"]!="group notification"]
    final_df=temp[temp["Message"]!="<Media omitted>"]
    f=open("stop_hinglish.txt","r")
    stop_words=f.read()
    
    
    if user=="Overall":
    
        
        words=[]

        for message in final_df["Message"]:             ###### remove stop words
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)    
                    
        newdf=pd.DataFrame(Counter(words).most_common(20)) 
        
    else:
        final_df=final_df[final_df["User"]==user]
        words=[]

        for message in final_df["Message"]:             ###### remove stop words
            for word in message.lower().split():
                if word not in stop_words:
                    words.append(word)    
                    
        newdf=pd.DataFrame(Counter(words).most_common(20))
        
        
               
    return newdf     


def emojis_get():
    pass  

def monthly_timeline(df,user):
        

        df['MonthNum'] = df['datetime'].dt.month

        
    
        if user!="Overall":
            
            df=df[df["User"]==user]
            
        
                
        timeline=df.groupby(["year","month","MonthNum"]).count()["Message"].reset_index()
        time=[]
        for i in range(timeline.shape[0]):

           time.append(timeline["month"][i]+"-"+ str(timeline["year"][i]))
        
        timeline["month-year"]=time
        
        return timeline
    
def daily_timeline(user,df):
    
    if user!="Overall":
            
            df=df[df["User"]==user]
            
    df["onlydate"]=df["datetime"].dt.date
    daily=df.groupby(["onlydate"]).count()["Message"].reset_index()
    return daily        
    
def weekly_activity(user,df):
    if user!="Overall":
            
            df=df[df["User"]==user]
            
    df["day_name"]=df["datetime"].dt.day_name()
       
    
    return df["day_name"].value_counts()                                 
    
def monthly_activity(user,df): 
    if user!="Overall":
            
        df=df[df["User"]==user]
            
     
      
   
    return df["month"].value_counts()                                    
       
def activity_heatmap(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap    
     
            
            
            