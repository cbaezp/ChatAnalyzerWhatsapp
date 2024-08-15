import re
import pandas as pd
from datetime import datetime


def parse_whatsapp_chat(file):
    pattern = r'(\[.*?\]) (.*?): (.*)'
    lines = file.read().decode("utf-8").splitlines()

    data = []
    for line in lines:
        match = re.match(pattern, line)
        if match:
            timestamp = match.group(1).strip('[]')
            sender = match.group(2)
            message = match.group(3)
            #Noticed that whatsapp uses the list below as placeholders for media.
            if message not in ["audio omitted", "image omitted", "video omitted"]:
                try:
                    date_time_obj = datetime.strptime(timestamp, '%m/%d/%y, %I:%M:%S %p')
                except ValueError:
                    date_time_obj = datetime.strptime(timestamp, '%d/%m/%y, %I:%M:%S %p')
                data.append([date_time_obj, sender, message])

    df = pd.DataFrame(data, columns=['Timestamp', 'Sender', 'Message'])
    return df
