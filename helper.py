from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extractor = URLExtract()

def total_messages(selected_user,dataframe):
    
    if selected_user != 'Overall':
        dataframe =  dataframe[dataframe['name'] == selected_user]    
    num_messages = dataframe.shape[0] #fetch the number of messages

    words = []
    for message in dataframe.messages:
        words.extend(message.split())  # fetch the number of words

    media_messages = dataframe[dataframe.messages == '<Media omitted>'].shape[0] # fetches number of media messages

    links = []
    for message in dataframe.messages:
        links.extend(extractor.find_urls(message)) # fetches the links
    

    
    return num_messages,len(words),media_messages,len(links)

def monthly_timeline(selected_user,dataframe): # retrns a dataframe based on month
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['name'] == selected_user]

    timeline = dataframe.groupby(['year', 'month', 'month_name']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,dataframe): # retrns a dataframe based on date
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['name'] == selected_user]

    daily_timeline = dataframe.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def day_month_timeline(selected_user,dataframe):    # retrns a dataframe based on day_name, and month_name
    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['name'] == selected_user]

    return dataframe['day_name'].value_counts(), dataframe['month_name'].value_counts()


def activity_heatmap(selected_user,dataframe):  # heatmap based on hour 

    if selected_user != 'Overall':
        dataframe = dataframe[dataframe['name'] == selected_user]

    user_heatmap = dataframe.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap


def most_busy_user(dataframe):
    x = dataframe['name'].value_counts().head()
    dataframe = round((dataframe['name'].value_counts()/len(dataframe))*100,2).reset_index().rename(columns = {'index':'Name','name':'Percent'})

    return x,dataframe

def create_wordcloud(selected_user,dataframe):
    f = open('english.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        dataframe =  dataframe[dataframe['name'] == selected_user]
    df_word = dataframe[dataframe['messages'] != '<Media omitted>']
    
    def remove_stop_words(messages):
        y = []
        for word in messages.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height= 500, min_font_size=10, background_color='white',max_font_size=70)
    df_word['messages'] = df_word['messages'].apply(remove_stop_words) 
    df_wc = wc.generate(df_word['messages'].str.cat(sep=" "))

    return df_wc


def most_words(selected_user,dataframe):

    if selected_user != 'Overall':
        dataframe =  dataframe[dataframe['name'] == selected_user]
    df_word = dataframe[dataframe['messages'] != '<Media omitted>']

    words = []
    for message in df_word.messages:
        for word in message.lower().split():
            if len(word) > 3:
                words.append(word)
    df_count = pd.DataFrame(Counter(words).most_common(20)).rename(columns={0:'Words',1:'val'})

    return df_count

def emoji_count(selected_user, dataframe):  
    if selected_user != 'Overall':
        dataframe =  dataframe[dataframe['name'] == selected_user]
    df_word = dataframe[dataframe['messages'] != '<Media omitted>']
    
    emojis = []
    for message in df_word.messages:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    df_emoji = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis)))).head(20).rename(columns= {0:"Emoji",1:"Count"})

    return df_emoji


