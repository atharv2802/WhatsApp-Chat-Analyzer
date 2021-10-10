import pandas as pd
import re

def chat_preprocessor(file_data):
    msg_pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(msg_pattern,file_data)[1:]
    dates = re.findall(msg_pattern, file_data)
    
    df = pd.DataFrame({'Member_Messages' : messages, 'message_date' : dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format= '%m/%d/%y, %H:%M - ')
    
    members = []
    messages = []
    for message in df['Member_Messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if (entry[1:]):
            K = 1 #kth occurrence
            n, m = message.split(":", K)
            members.append(n)
            messages.append(m)
        else:
            members.append('Group Notification')
            messages.append(entry[0])
            
    df['Member'] = members
    df['Message'] = messages
    df.drop(columns=['Member_Messages'], inplace=True)
    
    df['Year'] = df['message_date'].dt.year
    df['Month'] = df['message_date'].dt.month
    df['Month_Name'] = df['message_date'].dt.month_name()
    df['Day'] = df['message_date'].dt.day
    df['Day_Name'] = df['message_date'].dt.day_name()
    df['Hours'] = df['message_date'].dt.hour
    df['Minute'] = df['message_date'].dt.minute
    
    df.drop(columns=['message_date'], inplace=True)
    
    period = []
    for hour in df[['Day_Name', 'Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
            
    df['Period'] = period
    
    return df