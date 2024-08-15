import re

class ChatAnalyzer:
    def __init__(self, df):
        self.df = df
        self.df['Date'] = self.df['Timestamp'].dt.date
        self.df['Week'] = self.df['Timestamp'].dt.to_period('W').apply(lambda r: r.start_time)
        self.df['Month'] = self.df['Timestamp'].dt.to_period('M').apply(lambda r: r.start_time)

    def get_senders(self):
        return self.df['Sender'].unique().tolist()

    def filter_data(self, date_range, selected_senders, time_group):
        df_filtered = self.df[self.df['Sender'].isin(selected_senders)]
        if date_range:
            df_filtered = df_filtered[(df_filtered['Date'] >= date_range[0]) & (df_filtered['Date'] <= date_range[1])]
        
        if time_group == "day":
            df_filtered['TimeGroup'] = df_filtered['Date']
        elif time_group == "week":
            df_filtered['TimeGroup'] = df_filtered['Week']
        else:
            df_filtered['TimeGroup'] = df_filtered['Month']

        return df_filtered

    def get_message_count(self, df):
        return df.groupby(['TimeGroup', 'Sender']).size().unstack(fill_value=0)

    def get_conversation_length(self, df):
        df['Message_Length'] = df['Message'].apply(len)
        return df.groupby(['TimeGroup', 'Sender'])['Message_Length'].mean().unstack(fill_value=0)

    def get_response_time(self, df):
        df['Response_Time'] = df.groupby('Sender')['Timestamp'].diff().dt.total_seconds().div(60)
        df['Response_Time'] = df['Response_Time'].fillna(0)
        return df[df['Response_Time'] > 0]

    def get_initiation_pattern(self, df):
        df['Day'] = df['Timestamp'].dt.date
        initiator = df.groupby('Day')['Sender'].first().value_counts()
        return initiator

    def get_response_gaps(self, df):
        df['TimeDiff'] = df.groupby('Sender')['Timestamp'].diff().dt.total_seconds() / 3600
        df['TimeDiff'] = df['TimeDiff'].fillna(0)
        return df[df['TimeDiff'] >= 0]

    def get_emoji_frequency(self, df, emoji):
        df['Emoji_Count'] = df['Message'].apply(lambda x: x.count(emoji))
        df_emoji = df[df['Emoji_Count'] > 0]
        return df_emoji.groupby(['TimeGroup', 'Sender'])['Emoji_Count'].sum().reset_index(name='count')

    def get_word_frequency(self, df, word):
        df_word = df[df['Message'].str.contains(word, case=False)]
        return df_word.groupby(['TimeGroup', 'Sender']).size().reset_index(name='count')

    def get_all_unique_emojis(self):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F700-\U0001F77F"  # alchemical symbols
                                   u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                                   u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                                   u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                                   u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                                   u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                                   "]+", flags=re.UNICODE)
        all_emojis = re.findall(emoji_pattern, ' '.join(self.df['Message']))
        unique_emojis = set(''.join(sorted(all_emojis)))
        return sorted(unique_emojis)

    def perform_sentiment_analysis(self, df):
        #TODO:
        pass

    def get_time_series_data(self, df):
        return df.groupby('TimeGroup').size()
