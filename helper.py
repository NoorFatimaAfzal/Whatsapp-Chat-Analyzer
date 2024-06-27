from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import re

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    # fetch the most busy users
    x = df['User'].value_counts().head()
    df = round((df['User'].value_counts()/df.shape[0])*100)
    return x, df

def create_wordcloud(selected_user, df):

    f = open(r'C:\Users\InfoBay\OneDrive\Desktop\whatsapp_chat_analyzer\English + Urdu.txt', 'r')
    stop_words = f.read().split('\n')

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    temp = df[df['Message'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return ' '.join(y)
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['Message'] = temp['Message'].apply(remove_stopwords)
    df_wc = wc.generate(df['Message'].str.cat(sep=' '))

    return df_wc

def most_common_words(selected_user, df):

    f = open(r'C:\Users\InfoBay\OneDrive\Desktop\whatsapp_chat_analyzer\English + Urdu.txt', 'r')
    stop_words = f.read().split('\n')

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    
    temp = df[df['Message'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    words = []

    for messages in temp['Message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(10))

    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []
    emoji_regex = r'[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U00002639\U0001F9D0-\U0001F9FF]+'

    for message in df['Message']:
        emojis.extend(re.findall(emoji_regex, message))

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.items(), columns=['Emoji', 'Count']).sort_values(by='Count', ascending=False)

    return emoji_df


def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('Only date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['Day name'].value_counts()

def monthly_activity_map(selected_user,df):
    
        if selected_user != 'Overall':
            df = df[df['User'] == selected_user]
    
        return df['Month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    heatmap = df.pivot_table(index='Day name', columns='period', values='Message', aggfunc='count').fillna(0)

    return heatmap