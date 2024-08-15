import streamlit as st
from app.utils.file_parser import parse_whatsapp_chat
from app.analysis.chat_analyzer import ChatAnalyzer
from app.analysis.visualizer import Visualizer


def upload_file():
    st.markdown("""
    ### Instructions to Export WhatsApp Conversation
    1. Open WhatsApp on your mobile device.
    2. Select the chat you want to export.
    3. Tap on the three dots (menu) in the top-right corner.
    4. Select **More** and then tap **Export Chat**.
    5. Choose whether to export **Without Media** or **Include Media** (Select: Without Media).
    6. A zip file will be generated. Decompress the file and `.txt` will be extracted.
    7. Save the exported `.txt` file and upload it here.
    """)

    uploaded_file = st.file_uploader("Choose a TXT file", type=["txt"]) 
    if uploaded_file is not None:
        try:
            df = parse_whatsapp_chat(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error processing file: {e}")
            return None
    return None


def main():
    st.title("Chat Analyzer")
    df = upload_file()

    if df is not None:
        analyzer = ChatAnalyzer(df)
        visualizer = Visualizer(analyzer)

        # Sidebar filters
        first_date, last_date = df['Date'].min(), df['Date'].max()
        date_range = st.sidebar.date_input("Select date range", [first_date, last_date], min_value=first_date, max_value=last_date)

        selected_senders = st.sidebar.multiselect("Select senders", analyzer.get_senders(), default=analyzer.get_senders())
        time_group = st.sidebar.selectbox("Group by", ["day", "week", "month"])

        if selected_senders:
            df_filtered = analyzer.filter_data(date_range, selected_senders, time_group)

            # Display charts
            st.subheader("Frequency of Communication")
            st.markdown("This chart shows the number of messages sent by each sender over the selected time period. Use this chart to see who is more active in the conversation.")

            visualizer.plot_message_count(df_filtered, time_group)

            st.subheader("Avg. Conversation Length")
            st.markdown("This chart displays the average length of messages sent by each sender over time. It helps to identify who tends to write longer messages.")

            visualizer.plot_conversation_length(df_filtered, time_group)

            st.subheader("Average Response Time")
            st.markdown("This chart shows the average time each sender takes to respond to the other person's messages. It provides insights into responsiveness.")

            visualizer.plot_response_time(df_filtered, time_group)

            # This is a binary representaion, so currently does not react to the parameter. 
            # TODO:
            # Finde a better way to visualize this.
            st.subheader("Conversation Starter")
            st.markdown("This chart indicates who initiates conversations more frequently. It shows who usually starts the interaction.")

            visualizer.plot_initiation_pattern(df_filtered)

            st.subheader("Response Gaps")
            st.markdown("This chart displays the longest time gaps between consecutive messages from the same sender. Useful for identifying periods of inactivity.")

            visualizer.plot_response_gaps(df_filtered, time_group)

            st.subheader("Frequency of Emojis")
            st.markdown("This chart shows how often a selected emoji is used by each sender. It's useful for analyzing trends.")

            all_emojis = analyzer.get_all_unique_emojis()
            if all_emojis:
                emoji = st.selectbox("Select emoji", all_emojis)
                visualizer.plot_emoji_frequency(df_filtered, emoji, time_group)

            st.subheader("Frequency of Words")
            st.markdown("This chart displays how frequently a specific word or term is used by each sender. It's useful for analyzing trends.")

            word = st.text_input("Enter word/term")
            if word:
                visualizer.plot_word_frequency(df_filtered, word, time_group)

            # TODO:
            # st.subheader("Sentiment Analysis")
            # visualizer.plot_sentiment_analysis(df_filtered, time_group)
        else:
            st.error("Please select at least one sender.")

if __name__ == "__main__":
    main()
