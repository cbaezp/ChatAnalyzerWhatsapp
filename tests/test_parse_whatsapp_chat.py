import unittest
import pandas as pd
from io import BytesIO
from app.utils.file_parser import parse_whatsapp_chat  

class TestParseWhatsappChat(unittest.TestCase):

    def test_parse_standard_format(self):
        chat_data = b"[12/01/23, 03:45:12 p.m.] John: Hello!\n[12/01/23, 03:46:12 p.m.] Jane: Hi, how are you?"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['Sender'], 'John')
        self.assertEqual(df.iloc[1]['Sender'], 'Jane')

    def test_parse_non_standard_format(self):
        chat_data = b"[01/12/23, 03:45:12 p.m.] John: Hello!\n[01/12/23, 03:46:12 p.m.] Jane: Hi, how are you?"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['Sender'], 'John')
        self.assertEqual(df.iloc[1]['Sender'], 'Jane')

    def test_parse_day_month_format(self):
        chat_data = b"[12/01/23, 03:45:12 p.m.] John: Hello!\n[12/01/23, 03:46:12 p.m.] Jane: Hi, how are you?"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['Sender'], 'John')
        self.assertEqual(df.iloc[1]['Sender'], 'Jane')

    def test_parse_with_media_omitted(self):
        chat_data = b"[12/01/23, 03:45:12 p.m.] John: audio omitted\n[12/01/23, 03:46:12 p.m.] Jane: Hi, how are you?"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 1)  # One message should be skipped
        self.assertEqual(df.iloc[0]['Sender'], 'Jane')

    def test_invalid_date_format(self):
        chat_data = b"[99/99/99, 03:45:12 p.m.] John: Hello!"
        with self.assertRaises(ValueError):
            parse_whatsapp_chat(BytesIO(chat_data))

    def test_24_hour_format(self):
        chat_data = b"[23/05/2024 21:44:49] Alice: Good evening!\n[23/05/2024 08:30:15] Bob: Good morning!"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['Sender'], 'Alice')
        self.assertEqual(df.iloc[1]['Sender'], 'Bob')
    
    #not expected; but just in case
    def test_mixed_formats(self):
        chat_data = b"[12/01/23, 03:45:12 p.m.] John: Hello!\n[23/05/2024 21:44:49] Jane: How's it going?"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['Sender'], 'John')
        self.assertEqual(df.iloc[1]['Sender'], 'Jane')

    def test_omitted_media_multiple_entries(self):
        chat_data = b"[12/01/23, 03:45:12 p.m.] John: audio omitted\n[12/01/23, 03:46:12 p.m.] Jane: image omitted\n[12/01/23, 03:47:12 p.m.] John: How are you?"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 1)  # Two messages should be skipped
        self.assertEqual(df.iloc[0]['Sender'], 'John')
        self.assertEqual(df.iloc[0]['Message'], 'How are you?')

    def test_case_with_empty_file(self):
        chat_data = b""
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 0)  # DataFrame should be empty

    def test_case_with_only_media_omitted(self):
        chat_data = b"[12/01/23, 03:45:12 p.m.] John: audio omitted\n[12/01/23, 03:46:12 p.m.] Jane: video omitted"
        df = parse_whatsapp_chat(BytesIO(chat_data))
        self.assertEqual(len(df), 0)  # DataFrame should be empty as both messages are media omitted

if __name__ == '__main__':
    unittest.main()
