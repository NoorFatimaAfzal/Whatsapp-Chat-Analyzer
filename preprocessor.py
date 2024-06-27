import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apm]{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    timestamps = re.findall(pattern, data)

    df = pd.DataFrame({'User Message': messages, 'Message Date': timestamps})
    df['Message Date'] = pd.to_datetime(df['Message Date'], format='%d/%m/%Y, %I:%M %p - ')
    df.rename(columns={'Message Date': 'Date'}, inplace=True)

    users = []
    clean_messages = []  # renamed to avoid conflict with messages in original data

    for message in df['User Message']:
        # Use regex to split at the first ": " occurrence
        match = re.match(r'(.*?):\s(.*)', message)
        if match:
            users.append(match.group(1))
            clean_messages.append(match.group(2))
        else:
            users.append('Group Notification')
            clean_messages.append(message)

    df['User'] = users
    df['Message'] = clean_messages
    df.drop(columns=['User Message'], inplace=True)

    df['Only date'] = df['Date'].dt.date
    df['Year'] = df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Day name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['Day name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df