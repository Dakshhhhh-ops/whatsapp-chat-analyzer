import streamlit as st
import preprocessor
import helper

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

        num_messages, num_words, num_images, num_videos, num_audio, num_stickers, num_gifs = helper.fetch_stats(selected_box, df)

        col1, col2 = st.columns(2)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(num_words)

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