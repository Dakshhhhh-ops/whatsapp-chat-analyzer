from urlextract import URLExtract

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



