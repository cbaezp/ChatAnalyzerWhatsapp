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
           
                timestamp = timestamp.replace(' a.m.', ' AM').replace(' p.m.', ' PM').replace('a.m.', ' AM').replace('p.m.', ' PM')
                
                # List of possible date formats to handle various cases
                date_formats = [
                    '%m/%d/%y, %I:%M:%S %p',  # 08/12/24, 8:57:27 PM
                    '%d/%m/%y, %I:%M:%S %p',  # 12/08/24, 8:57:27 PM
                    '%d/%m/%Y %H:%M:%S',      # 23/05/2024 21:44:49 (24-hour format)
                    '%m/%d/%y, %I:%M:%S %p',  # 08/12/24, 08:57:27 AM
                    '%d/%m/%y, %I:%M:%S %p',  # 12/08/24, 08:57:27 AM
                    '%d/%m/%y, %H:%M:%S',     # 23/05/24, 21:44:49 (24-hour format)
                    '%d/%m/%Y, %H:%M:%S',     # 23/05/2024, 21:44:49 (24-hour format with full year)
                    '%m/%d/%Y, %I:%M:%S %p'   # 08/12/2024, 8:57:27 PM
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
