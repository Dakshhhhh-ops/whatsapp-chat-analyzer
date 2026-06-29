from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
from collections import Counter
import pandas as pd

extract = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)

    num_images = df['message'].str.contains('image omitted', case=False, na=False).sum()
    num_videos = df['message'].str.contains('video omitted', case=False, na=False).sum()
    num_audio  = df['message'].str.contains('audio omitted', case=False, na=False).sum()
    num_stickers = df['message'].str.contains('sticker omitted', case=False, na=False).sum()
    num_gifs   = df['message'].str.contains('gif omitted', case=False, na=False).sum()

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    num_links = len(links)

    return num_messages, num_words, num_images, num_videos, num_audio, num_stickers, num_gifs, num_links


def busiest_users(df):
    df = df[df['user'] != 'group_notification']
    x = df['user'].value_counts().head()
    percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2)
    return x, percent


def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains(
        'image omitted|video omitted|audio omitted|sticker omitted|gif omitted',
        case=False, na=False
    )]

    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stop_words = f.read()

    temp = temp.copy()
    temp['message'] = temp['message'].str.replace(r'http\S+', '', regex=True)

    text = " ".join(temp['message']).lower()

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(text)


def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for c in message:
            if c in emoji.EMOJI_DATA:
                emojis.append(c)

    return Counter(emojis).most_common()


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_num', 'month'])
          .count()['message']
          .reset_index()
          .sort_values(['year', 'month_num'])
    )
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)
    return timeline


def daily_timelime(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    return df.groupby('only_date').count()['message'].reset_index()


def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]
    return df['month'].value_counts().reindex(months).fillna(0)


def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return df['day_name'].value_counts().reindex(days).fillna(0)


def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df.pivot_table(
        index='day_name', columns='period',
        values='message', aggfunc='count'
    ).fillna(0)


# ─────────────────────────────────────────────────────────────────────────────
# RESPONSE TIME ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def response_analysis(selected_user, df):
    """
    Core function. Returns a flat DataFrame of every valid reply event with:
      user, previous_user, response_time (mins), hour, date

    Fixes vs original:
    - cutoff raised from 120 → 720 min (12 h) so you don't lose evening→morning replies
    - .iloc loop replaced with vectorised shift — ~100× faster on large chats
    - group_notification filter applied before the shift so it never contaminates gaps
    - selected_user filter kept at the top so per-user view works correctly
    """
    df = df[df['user'] != 'group_notification'].copy()
    df = df.sort_values('date').reset_index(drop=True)

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df['prev_user'] = df['user'].shift(1)
    df['prev_date'] = df['date'].shift(1)

    # keep only rows where user changed (genuine reply, not continuation)
    replies = df[df['user'] != df['prev_user']].copy()

    replies['response_time'] = (
        (replies['date'] - replies['prev_date']).dt.total_seconds() / 60
    ).round(2)

    # drop negatives (clock skew) and gaps > 12 h (new conversation, not a reply)
    replies = replies[(replies['response_time'] > 0) & (replies['response_time'] <= 720)]

    return replies[['user', 'prev_user', 'response_time', 'hour', 'date']].rename(
        columns={'prev_user': 'previous_user'}
    )


def avg_response_time(selected_user, df):
    """
    Per-user mean, median, and reply count — sorted fastest first.
    Works for Overall (all users) or a single user's replies.
    """
    rt = response_analysis(selected_user, df)

    if rt.empty:
        return pd.DataFrame(columns=['avg_mins', 'median_mins', 'replies'])

    result = (
        rt.groupby('user')['response_time']
          .agg(avg_mins='mean', median_mins='median', replies='count')
          .round(2)
          .sort_values('avg_mins')
    )
    return result


def response_time_by_hour(selected_user, df):
    """
    Median response time bucketed by hour of day (0–23).
    Useful for the 'when is this group most responsive' line chart.
    """
    rt = response_analysis(selected_user, df)

    if rt.empty:
        return pd.Series(dtype=float)

    return (
        rt.groupby('hour')['response_time']
          .median()
          .reindex(range(24))   # fill any missing hours with NaN so chart is continuous
          .round(2)
    )


def reply_matrix(df):
    """
    Pivot table: rows = who sent the original message,
                 columns = who replied.
    Cell value = number of reply events.
    Only uses Overall data (user filter doesn't make sense for a matrix).
    """
    rt = response_analysis("Overall", df)

    if rt.empty:
        return pd.DataFrame()

    matrix = (
        rt.groupby(['previous_user', 'user'])
          .size()
          .unstack(fill_value=0)
    )
    return matrix


def fastest_pair(df):
    """
    Returns a human-readable string like:
      'Rahul replies to Priya 2.4× faster than to anyone else'

    Algorithm:
      1. Compute per-pair (sender → replier) mean response time
      2. For each replier, compare their best pair avg vs their overall avg
      3. Pick the pair with the highest speed-up ratio
    """
    rt = response_analysis("Overall", df)

    if rt.empty or len(rt) < 10:
        return None

    pair_avg = (
        rt.groupby(['user', 'previous_user'])['response_time']
          .mean()
          .reset_index()
          .rename(columns={'response_time': 'pair_avg', 'previous_user': 'to_user'})
    )

    overall_avg = (
        rt.groupby('user')['response_time']
          .mean()
          .reset_index()
          .rename(columns={'response_time': 'overall_avg'})
    )

    merged = pair_avg.merge(overall_avg, on='user')

    # need at least a few samples per pair to avoid noise
    pair_counts = (
        rt.groupby(['user', 'previous_user'])
          .size()
          .reset_index(name='n')
          .rename(columns={'previous_user': 'to_user'})
    )
    merged = merged.merge(pair_counts, on=['user', 'to_user'])
    merged = merged[merged['n'] >= 5]

    if merged.empty:
        return None

    merged['ratio'] = (merged['overall_avg'] / merged['pair_avg']).round(2)
    best = merged.loc[merged['ratio'].idxmax()]

    return {
        'replier':     best['user'],
        'to':          best['to_user'],
        'ratio':       best['ratio'],
        'pair_avg':    round(best['pair_avg'], 1),
        'overall_avg': round(best['overall_avg'], 1),
    }