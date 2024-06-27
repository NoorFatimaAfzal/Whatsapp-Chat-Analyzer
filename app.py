import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analysis')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['User'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button('Show Analysis'):

        num_messages, words, media_messages, no_of_links = helper.fetch_stats(selected_user, df)
        st.title('Whatsapp Chat Analysis - Top statistics')
        col1,col2, col3, col4 = st.columns(4)
        
        with col1:
            st.title('Total Messages')
            st.title(num_messages)

        with col2:
            st.title('Total Words')
            st.title(words)

        with col3:
            st.title('Total Media Shared')
            st.title(media_messages)

        with col4:
            st.title('Total Links Shared')
            st.title(no_of_links)

        # Monthly Timeline
        timeline = helper.monthly_timeline(selected_user, df)
        st.title('Monthly Timeline')
        fig, ax = plt.subplots()
        ax.plot(timeline['Time'], timeline['Message'], color='green', marker='o')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        daily_timeline = helper.daily_timeline(selected_user, df)
        st.title('Daily Timeline')
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['Only date'], daily_timeline['Message'], color='blue', marker='o')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)
        
        with col1:
            st.header('Most busy Days')
            busy_days = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_days.index, busy_days.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most busy Months')
            busy_months = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_months.index, busy_months.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap, annot=True)
        st.title('Activity Heatmap')
        st.pyplot(fig)
        
        # most busy users
        if selected_user == 'Overall':
            st.subheader('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        st.title('Word Cloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # emoji analysis
        st.title('Emoji Analysis')
        emojis = helper.emoji_helper(selected_user, df)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df.head()['Count'], labels=emoji_df.head()['Emoji'], autopct="%0.2f")
            ax.set_title('Top Emojis Used')
            st.pyplot(fig)
