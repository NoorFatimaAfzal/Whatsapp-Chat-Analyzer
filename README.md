# WhatsApp Chat Analysis with Streamlit

This Streamlit app analyzes WhatsApp chat data, providing insights such as message statistics, timelines, activity maps, word clouds, and emoji analysis.

## Features

- **Total Messages, Words, Media Shared, Links Shared**: Displays key statistics based on selected user.
- **Monthly Timeline**: Shows message frequency over months.
- **Daily Timeline**: Displays message frequency over days.
- **Activity Map**: Highlights busiest days and months.
- **Activity Heatmap**: Visualizes activity patterns throughout the day.
- **Most Busy Users**: Lists most active users in the chat.
- **Word Cloud**: Generates a word cloud based on selected user's messages.
- **Most Common Words**: Shows the most frequently used words.
- **Emoji Analysis**: Analyzes and visualizes emoji usage.

## Usage

1. Upload your WhatsApp chat export file.
2. Select a user or 'Overall' for overall chat analysis.
3. Click 'Show Analysis' to generate insights.
4. Explore different visualizations and analyses based on the selected user.

## Installation

To run the app locally:

1. Clone the repository.
2. Install the necessary dependencies:
   ```bash
   pip install streamlit matplotlib seaborn pandas
