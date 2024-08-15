# Chat Analyzer

## Overview

The Chat Analyzer is a Streamlit-based application designed to analyze WhatsApp chat exports. It provides various analytical insights such as frequency of communication, average conversation length, response time, interaction patterns, emoji usage, word frequency, and sentiment analysis. The tool is useful for visualizing and understanding conversation dynamics.

## Features

- **Frequency of Communication**: Analyze the number of messages sent by each participant over time.
- **Conversation Length**: Visualize the average length of messages over a selected time period.
- **Average Response Time**: Measure how quickly each participant responds to messages.
- **Interaction Patterns**: Identify who initiates conversations more often.
- **Response Gaps**: Highlight periods of inactivity or delayed responses.
- **Emoji Frequency**: Track how often specific emojis are used by each participant.
- **Word Frequency**: Analyze the frequency of specific words or phrases.
- **Sentiment Analysis**: Evaluate the emotional tone of the conversation over time (PENDING).

## How to Use

### Prerequisites

Ensure you have Python 3.7 or later installed on your machine. You'll also need to install the required Python packages.

### Installation

1. **Clone the Repository**

   git clone https://github.com/cbaezp/ChatAnalyzerWhatsapp.git
   cd chat-analyzer

2. **Create a Virtual Environment**

   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. **Install the Dependencies**

   pip install -r requirements.txt

### Running the Application

To start the Chat Analyzer application, run:

   streamlit run streamlit_app.py

### Exporting WhatsApp Chat

To analyze your WhatsApp chat, follow these steps to export it:

1. Open WhatsApp on your mobile device.
2. Select the chat you want to export.
3. Tap on the three dots (menu) in the top-right corner.
4. Select **More** and then tap **Export Chat**.
5. Choose whether to export **Without Media** (recommended) or **Include Media**.
6. Save the exported `.txt` file and upload it in the application.

### Uploading the Chat File

1. On the application's home page, upload your WhatsApp chat `.txt` file.
2. Select the desired analysis parameters (date range, participants, grouping by day/week/month).
3. View the generated charts and insights based on the chat data.


## Contributing

If you would like to contribute to this project, please feel free to submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project was built using [Streamlit](https://streamlit.io/).
