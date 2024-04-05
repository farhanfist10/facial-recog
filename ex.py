import whisper
import re
import heapq
import whisper
import os
from pytube import YouTube
from pathlib import Path
import shutil
import pandas as pd
from googletrans import Translator

import streamlit as st
import re
import heapq
import whisper
import os
from pytube import YouTube
from pathlib import Path
import shutil
import pandas as pd


@st.cache_resource
def load_model():
    model = whisper.load_model("base")
    return model

def save_video(url, video_filename):
    youtubeObject = YouTube(url)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download()
    except:
        print("An error has occurred")
    print("Download is completed successfully")
    
    return video_filename

def save_audio(url):
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    base, ext = os.path.splitext(out_file)
    file_name = base + '.mp3'
    try:
        os.rename(out_file, file_name)
    except WindowsError:
        os.remove(file_name)
        os.rename(out_file, file_name)
    audio_filename = Path(file_name).stem+'.mp3'
    video_filename = save_video(url, Path(file_name).stem+'.mp4')
    print(yt.title + " Has been successfully downloaded")
    return yt.title, audio_filename, video_filename

def audio_to_transcript(audio_file):
    model = load_model()
    result = model.transcribe(audio_file)
    transcript = result["text"]
    return transcript
    
st.set_page_config(layout="wide")
           
st.subheader("Video Summary With OpenAI")
url =  st.text_input('Enter URL of YouTube video:')
    # if upload_video is not None:
if st.button("Analyze Video"):
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.info("Video uploaded successfully")
            video_title, audio_filename, video_filename = save_audio(url)
            st.video(video_filename)
        with col2:
            st.info("Transcript is below") 
            print(audio_filename)
            transcript_result = audio_to_transcript(audio_filename)
            st.success(transcript_result)
        with col3:
            st.info("Topic Modeling and Labeling")
            # labeling_text = transcript_result
            # # industry = label_topic(labeling_text)
            # st.markdown("**Topic Labeling Industry Wise**")
            # st.write(industry)
