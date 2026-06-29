import re
import pandas as pd
def preprocess(data):
    pattern = r'\[(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM))\]\s'

    messages = re.split(pattern, data)[1:]
    dates = messages[0::2]
    msgs = messages[1::2]

    df = pd.DataFrame({
    'date': dates,
    'message': msgs
    })

    users = []
    messages = []
    for message in df['message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df['date'] = pd.to_datetime(df['date'])

    df['message'] = df['message'].str.strip()

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # period column
    period = []

    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour:02d}-{hour+1:02d}")

    df['period'] = period

    return df
        

