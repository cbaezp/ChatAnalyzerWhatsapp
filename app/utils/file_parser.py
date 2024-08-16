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
            # Check if the message is not a placeholder for media
            if message not in ["audio omitted", "image omitted", "video omitted"]:
                # Normalize the timestamp by replacing "a.m." and "p.m." with "AM" and "PM"
                timestamp = timestamp.replace(' a.m.', ' AM').replace(' p.m.', ' PM').replace('a.m.', ' AM').replace('p.m.', ' PM')
                
                # List of possible date formats to handle various cases
                date_formats = [
                    '%m/%d/%y, %I:%M:%S %p',
                    '%d/%m/%y, %I:%M:%S %p'
                ]
                
                for date_format in date_formats:
                    try:
                        date_time_obj = datetime.strptime(timestamp, date_format)
                        break
                    except ValueError:
                        continue
                else:
                    # If no format matched, raise an error or handle it accordingly
                    raise ValueError(f"Timestamp format not recognized: {timestamp}")
                
                data.append([date_time_obj, sender, message])

    df = pd.DataFrame(data, columns=['Timestamp', 'Sender', 'Message'])
    return df
