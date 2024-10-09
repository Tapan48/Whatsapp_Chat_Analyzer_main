import pandas as pd

def extract_user_and_message(row):
    if ':' in row['User_Message']:
        user, message = row['User_Message'].split(':', 1)
    else:
        user = 'group notification'
        message = row['User_Message']
    return pd.Series({'User': user.strip(), 'Message': message.strip()})



def preprocess(string_data):
      # Split string into lines
    lines = string_data.splitlines()
     # Create empty list
    data = []
    
    # Loop over lines and extract datetime and user/message
    for line in lines:
        line = line.strip()
        if len(line) > 0:
            parts = line.split('-', maxsplit=1)
            if len(parts) == 2:
                datetime_str = parts[0].strip()
                user_message_str = parts[1].strip()
                data.append((datetime_str, user_message_str))
    
    # Create pandas DataFrame
    df = pd.DataFrame(data, columns=['Date-Time', 'User_Message'])
    
    df[['User', 'Message']] = df.apply(extract_user_and_message, axis=1)
    df=df.drop(columns={"User_Message"})
    df=df.rename(columns={"Date-Time":"datetime"})
    # remove rows with incorrect format
    df = df[df['datetime'].str.match('\d{2}/\d{2}/\d{4}, \d{2}:\d{2}')]

    # convert the datetime column to a datetime object
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d/%m/%Y, %H:%M')
    df["year"]=df["datetime"].dt.year
    df["month"]=df["datetime"].dt.month_name()
    df["date"]=df["datetime"].dt.day
    df["day_name"]=df["datetime"].dt.day_name()
    df["hour"]=df["datetime"].dt.hour
    df["minute"]=df["datetime"].dt.minute
    
    period=[]
    for hour in df["hour"]:

        if hour==23:
            period.append(str(hour)+"-"+"00")
            
        elif hour==0:
            period.append("00"+"-"+"1")
            
        else:
            period.append(str(hour)+"-"+str(hour+1))
            
            
    df["period"]=period
    
    return df
    
    
