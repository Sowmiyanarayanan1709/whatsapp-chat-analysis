import re
import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    for i in range(len(dates)):  # stripping off the unwanted characters
        dates[i] = dates[i].strip('- ')

    df = pd.DataFrame({'user_message': messages, 'Date': dates})
    df['Date'] = pd.to_datetime(df['Date'])
    df['year'] = df['Date'].dt.year
    df['month_name'] = df['Date'].dt.month_name()
    df['month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['day_name'] = df['Date'].dt.day_name()
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    df['only_date'] = df['Date'].dt.date

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour+1))
        else:
            period.append(str(hour) + "-" + str(hour+1))
    df['period'] = period
    
    name = []
    message = []

    for i in range(len(messages)):  
        splitted_message = messages[i].split(':',1)  # splitting the message to get the actual message and the user name
        if len(splitted_message) == 2:
            name.append(splitted_message[0])
            message.append(splitted_message[1])
            
        else:
            name.append('Group notfication')
            message.append(splitted_message[0])
            
        
    for i in range(len(messages)):    # stripping the extra spaces in the message
        message[i] = message[i].strip('\n')
        message[i] = message[i].strip(' ')
        
    df = df.drop(['user_message'],axis = 1)
    df.insert(0,column = 'name',value = name)
    df.insert(1,column = 'messages', value = message)

    return df