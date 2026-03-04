from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji






def fetch_stats(selected_user,df):
    
    if selected_user != "Overall": # If there is analyz on specific user
        
        df = df[df['user']== selected_user] # df = specific user
    
    #Fetch the total Number of Message    
    num_messages = df.shape[0]
    
    # fetch the total number of words
    words = []   ## Same previous  logic apply here
    for message in df['message']:
        words.extend(message.split())
        
        
    # Fetch the number of media message (images)
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    
    
    # Fetch the Number of links shared
    extract = URLExtract()
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
            
    return num_messages,len(words),num_media_messages,len(links)
    
    
def most_busy_user(df):
    x = df['user'].value_counts().head()  #most busy user
    ## Total Percentage of total message
    df= round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'user':'name','count':'percent'})
    return x,df
    

#WordCloud
def create_wordcloud(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    
    return df_wc


# Most Common Words
def most_common_words(selected_user,df):
    
    f= open('stop_hinglish.txt','r')
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    ##remove  group notification

    temp = df[df['user'] != 'group_notification']

    ## Remove Media ommited 

    temp = temp[temp['message'] != '<Media omitted>\n']
    
    ## Remove Stop Words
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
                
    most_common_df= pd.DataFrame(Counter(words).most_common(20), columns=['Word','No of Times'])
    return most_common_df


# Most Common Emojis
def  emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emojis','No of Times'])
    
    return emoji_df

### Monthly timeline
def monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+ str(timeline['year'][i]))
        
    timeline['time'] = time
        
    return timeline

## Daily timeline
def daily_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    
    return daily_timeline

## Weekly Activity map
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    return df['day_name'].value_counts()


## Monthly Activity map
def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    return df['month'].value_counts()


## Activity HeatMap
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user']== selected_user] # df = specific user
        
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap