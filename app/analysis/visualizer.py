import streamlit as st
import altair as alt


class Visualizer:
    def __init__(self, analyzer):
        self.analyzer = analyzer

    def plot_message_count(self, df, time_group):
        message_count = self.analyzer.get_message_count(df)
        st.bar_chart(message_count)

    def plot_conversation_length(self, df, time_group):
        message_length = self.analyzer.get_conversation_length(df)
        st.line_chart(message_length)

    def plot_response_time(self, df, time_group):
        response_time = self.analyzer.get_response_time(df)
        if not response_time.empty:
            response_time_grouped = (
                response_time.groupby(["TimeGroup", "Sender"])["Response_Time"]
                .mean()
                .reset_index()
            )
            chart = (
                alt.Chart(response_time_grouped)
                .mark_line(point=True)
                .encode(
                    x="TimeGroup:T",
                    y=alt.Y("Response_Time:Q", title="Avg Response Time (mins)"),
                    color="Sender:N",
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No response time data available.")

    def plot_initiation_pattern(self, df):
        initiation_pattern = self.analyzer.get_initiation_pattern(df)
        st.bar_chart(initiation_pattern)

    def plot_response_gaps(self, df, time_group):
        response_gaps = self.analyzer.get_response_gaps(df)
        if not response_gaps.empty:
            response_gaps_grouped = (
                response_gaps.groupby(["TimeGroup", "Sender"])["TimeDiff"]
                .max()
                .reset_index()
            )
            chart = (
                alt.Chart(response_gaps_grouped)
                .mark_line(point=True)
                .encode(
                    x="TimeGroup:T",
                    y=alt.Y("TimeDiff:Q", title="Max Response Gap (hours)"),
                    color="Sender:N",
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No response gap data available.")

    def plot_emoji_frequency(self, df, emoji, time_group):
        emoji_frequency = self.analyzer.get_emoji_frequency(df, emoji)
        if not emoji_frequency.empty:
            chart = (
                alt.Chart(emoji_frequency)
                .mark_bar()
                .encode(
                    x="TimeGroup:T",
                    y="count:Q",
                    color="Sender:N",
                    tooltip=["Sender", "count"],
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available for the selected emoji.")

    def plot_word_frequency(self, df, word, time_group):
        word_frequency = self.analyzer.get_word_frequency(df, word)
        if not word_frequency.empty:
            chart = (
                alt.Chart(word_frequency)
                .mark_bar()
                .encode(
                    x="TimeGroup:T",
                    y="count:Q",
                    color="Sender:N",
                    tooltip=["Sender", "count"],
                )
                .interactive()
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("No data available for the selected word/term.")

    def plot_sentiment_analysis(self, df, time_group):
        #TODO
        pass
