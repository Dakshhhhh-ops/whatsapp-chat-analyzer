import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import pandas as pd

st.sidebar.title("Whatsapp chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_box = st.sidebar.selectbox("Show analysis", user_list)

    # Store button click in session state
    if st.sidebar.button("Show analysis"):
        st.session_state.show_analysis = True

    # Show analysis if button has been clicked once
    if 'show_analysis' in st.session_state and st.session_state.show_analysis:

        num_messages, num_words, num_images, num_videos, num_audio, num_stickers, num_gifs, num_links = helper.fetch_stats(selected_box, df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

        with col3:
            st.header("Links Shared")
            st.title(num_links)

        st.subheader("Media Breakdown")

        media_type = st.selectbox(
            "Select Media Type",
            ["Images", "Videos", "Audio", "Stickers", "GIFs"]
        )

        if media_type == "Images":
            st.write("Images")
            st.title(num_images)

        elif media_type == "Videos":
            st.write("Videos")
            st.title(num_videos)

        elif media_type == "Audio":
            st.write("Audio")
            st.title(num_audio)

        elif media_type == "Stickers":
            st.write("Stickers")
            st.title(num_stickers)

        elif media_type == "GIFs":
            st.write("GIFs")
            st.title(num_gifs)

        #finding busiest user
        if selected_box=="Overall":
            x, percent=helper.busiest_users(df)

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(percent)

            with col2:
                fig, ax = plt.subplots(figsize=(8,5))
                ax.barh(x.index, x.values)

                ax.set_xlabel("Messages")
                ax.set_ylabel("Users")
                ax.set_title("Top 5 Most Active Users")

                st.pyplot(fig)
        

        st.title("Word Cloud")

        df_wc = helper.create_wordcloud(selected_box, df)

        fig, ax = plt.subplots()

        ax.imshow(df_wc)
        ax.axis("off")

        st.pyplot(fig)

        st.title("Emoji Analysis")

        emoji_df = helper.emoji_helper(selected_box, df)

        emoji_df = pd.DataFrame(
            emoji_df,
            columns=['emoji', 'count']
        )

        st.subheader("Top 10 Emojis")
        st.dataframe(
            emoji_df.head(10),
            use_container_width=True
        )

        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_box, df)

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(timeline['time'], timeline['message'], marker='o')

        plt.xticks(rotation=45)

        st.pyplot(fig)
        