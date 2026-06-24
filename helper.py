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


