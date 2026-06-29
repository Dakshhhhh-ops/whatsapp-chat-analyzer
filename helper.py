from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    num_messages=df.shape[0]
    

    words=[]
    for message in df['message']:
        words.extend(message.split())

    num_words=len(words)


    num_images = df['message'].str.contains(
    'image omitted',
    case=False,
    na=False
    ).sum()

    num_videos = df['message'].str.contains(
        'video omitted',
        case=False,
        na=False
    ).sum()

    num_audio = df['message'].str.contains(
        'audio omitted',
        case=False,
        na=False
    ).sum()

    num_stickers = df['message'].str.contains(
        'sticker omitted',
        case=False,
        na=False
    ).sum()

    num_gifs = df['message'].str.contains(
        'gif omitted',
        case=False,
        na=False
    ).sum()

    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    num_links=len(links)    
    return (
    num_messages,
    num_words,
    num_images,
    num_videos,
    num_audio,
    num_stickers,
    num_gifs,
    num_links
    )

def busiest_users(df):

    df = df[df['user'] != 'group_notification']

    x = df['user'].value_counts().head()

    percent = round(
        (df['user'].value_counts() / df.shape[0]) * 100,
        2
    )

    return x, percent

def create_wordcloud(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notification']
    temp = temp[
    ~temp['message'].str.contains(
        'image omitted|video omitted|audio omitted|sticker omitted|gif omitted',
        case=False,
        na=False
    )
]
    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()

    temp['message'] = temp['message'].str.replace(
    r'http\S+',
    '',
    regex=True
)

    text=" ".join(temp['message'])
    text=text.lower()

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=10,
        background_color='white'
    )
    df_wc=wc.generate(text)
    return df_wc

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.append(c)

    emoji_df=Counter(emojis).most_common()
    
    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_num', 'month'])
          .count()['message']
          .reset_index()
    )

    timeline = timeline.sort_values(['year', 'month_num'])

    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline


def daily_timelime(selected_user, df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]

    timeline = df.groupby('only_date').count()['message'].reset_index()

    return timeline

def month_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    month_counts = df['month'].value_counts()

    return month_counts.reindex(months).fillna(0)

def week_activity_map(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    days = [
        "Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday", "Sunday"
    ]

    day_counts = df['day_name'].value_counts()

    return day_counts.reindex(days).fillna(0)

def activity_heatmap(selected_user, df):

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    

    heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)
    

    return heatmap
