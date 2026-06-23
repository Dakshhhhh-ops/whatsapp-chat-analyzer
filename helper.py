

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

    return (
    num_messages,
    num_words,
    num_images,
    num_videos,
    num_audio,
    num_stickers,
    num_gifs
    )



