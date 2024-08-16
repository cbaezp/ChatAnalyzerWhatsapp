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
            
            # Check if the message is not a placeholder for media; might need to additional strings for stickers, calls, etc.
            if message not in ["audio omitted", "image omitted", "video omitted"]:
                
                # Normalize different AM/PM representations
                timestamp = timestamp.replace(' a.m.', ' AM').replace(' p.m.', ' PM')
                timestamp = timestamp.replace('a. m.', ' AM').replace('p. m.', ' PM')
                timestamp = timestamp.replace('a.m.', ' AM').replace('p.m.', ' PM')
                
                # List of possible date formats to handle various cases
                date_formats = [
                    '%m/%d/%y, %I:%M:%S %p',  # 08/12/24, 8:57:27 PM
                    '%d/%m/%y, %I:%M:%S %p',  # 12/08/24, 8:57:27 PM
                    '%d/%m/%Y %H:%M:%S',      # 23/05/2024 21:44:49 (24-hour format)
                    '%m/%d/%y, %I:%M:%S %p',  # 08/12/24, 08:57:27 AM
                    '%d/%m/%y, %I:%M:%S %p',  # 12/08/24, 08:57:27 AM
                    '%d/%m/%y, %H:%M:%S',     # 23/05/24, 21:44:49 (24-hour format)
                    '%d/%m/%Y, %H:%M:%S',     # 23/05/2024, 21:44:49 (24-hour format with full year)
                    '%m/%d/%Y, %I:%M:%S %p',  # 08/12/2024, 8:57:27 PM
                    '%H:%M, %d/%m/%Y',        # 10:03, 12/3/2024
                    '%H:%M, %m/%d/%Y',        # 10:03, 3/12/2024 (US format)
                    '%H:%M, %d/%m/%y',        # 10:03, 12/3/24 (short year format)
                    '%H:%M, %m/%d/%y',        # 10:03, 3/12/24 (short year, US format)
                    '%I:%M %p, %d/%m/%Y',     # 0:28 PM, 22/8/2022 (Handling AM/PM format with day/month/year)
                    '%I:%M %p, %m/%d/%Y',     # 0:28 PM, 8/22/2022 (US format)
                    '%I:%M %p, %d/%m/%y',     # 0:28 PM, 22/8/22 (short year format)
                    '%I:%M %p, %m/%d/%y',     # 0:28 PM, 8/22/22 (short year, US format)
                    '%I:%M %p, %d/%m/%Y',     # 0:28 p.m., 22/8/2022
                ]
                
                for date_format in date_formats:
                    try:
                        date_time_obj = datetime.strptime(timestamp, date_format)
                        break
                    except ValueError:
                        date_time_obj = None
                
                if date_time_obj is None:
                    continue  
                
                data.append([date_time_obj, sender, message])

    df = pd.DataFrame(data, columns=['Timestamp', 'Sender', 'Message'])
    return df
