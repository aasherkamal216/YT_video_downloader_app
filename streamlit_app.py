import streamlit as st
from pytube import YouTube
from stqdm import stqdm
import os
from pathlib import Path

def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def download_video(url, resolution):
    try:
        # Display message while fetching video details
        st.info("Fetching video details... Please wait.")

        # Get YouTube video
        yt = YouTube(url)

        # Display video details
        st.success(f"🎬 Video Title: {yt.title}")
        st.image(yt.thumbnail_url, caption="Thumbnail", use_column_width=True)
        st.success(f"⏱️ Video Duration: {yt.length} seconds")

        # Display message while downloading
        with st.spinner("Downloading your video... Please wait."):
            # Filter and select the desired resolution
            stream = yt.streams.filter(res=resolution, file_extension="mp4").first()

            # Sanitize the filename
            video_title = sanitize_filename(yt.title)

            # Remove any invalid characters from the video URL
            video_url_filename = sanitize_filename(url)

            # Combine the sanitized title and URL to create a unique filename
            filename = f"{video_title}_{video_url_filename}.mp4"

            # Get the file size for progress calculation
            total_size = stream.filesize

            # Specify the common directory in the user's home directory
            common_directory = Path(os.path.expanduser("~"))

            # Use stqdm to create a progress bar
            with stqdm(total=total_size, desc=f"Downloading {filename}", unit="B", unit_scale=True, unit_divisor=1024) as bar:
                # Download the video to the common directory
                stream.download(output_path=common_directory, filename=filename)
                # Update the progress bar in the Streamlit app
                bar.update(total_size)

        # Display success message
        st.success(f"✅ Download successful! The video is saved in the home directory as: {filename}")
    except Exception as e:
        # Display error message if an exception occurs
        st.error(f"❌ An error occurred: {e}")

def main():
    # Set app title
    st.title("YouTube Video Downloader🚀🌟")

    # User input for YouTube video URL
    url = st.text_input("Enter YouTube Video URL:")

    # Display the video details only if the URL is provided
    if url:
        # Fetch available resolutions dynamically
        yt = YouTube(url)
        available_resolutions = [str(stream.resolution) for stream in yt.streams.filter(file_extension="mp4")]

        # Resolution selection dropdown
        resolution = st.selectbox("Select Resolution:", available_resolutions)

        # Download button triggers the download_video function
        if st.button("Download"):
            download_video(url, resolution)

if __name__ == "__main__":
    # Run the app
    main()
