from pytubefix import YouTube
import logging
from django.conf import settings
import os
import assemblyai as aai
from ai21 import AI21Client
from ai21.models.chat import ChatMessage
from django.http import JsonResponse

def get_yt_link(link):
    yt = YouTube(link)
    title = yt.title
    return title

def download_audio(link):
    try:
        yt = YouTube(link)
        audio_file = yt.streams.get_audio_only()
        if(audio_file):
            out_file = audio_file.download(mp3=True, output_path=settings.MEDIA_ROOT)
        else:
            return JsonResponse({'error': 'Failed fetching audio file from yt link.'}, status=500)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
        
    return out_file

def get_transcription(link):
    audio_file = download_audio(link)
    aai.settings.api_key = '17fa4402e5ee49cdadca9595edbcb8dc'
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    
    return transcript.text

def generate_blog_from_transcription(transcript):
    client = AI21Client(api_key='dKcuxBft3Uh2BaAjcHktV9sLFPCPnCeS')
    
    messages = [
        ChatMessage(
            role="user",
            content=f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video:\n\n{transcript}\n\nArticle:"
        )
    ]
    
    #prompt = f"Based on the following transcript from a YouTube video, write a comprehensive blog article, write it based on the transcript, but dont make it look like a youtube video, make it look like a proper blog article and also your response will be pasted as .innerHtml so format it properly:\n\n{transcript}\n\nArticle:"

    response = client.chat.completions.create(
        model = "jamba-instruct",
        messages = messages,
        top_p=1.0
    )
    
    response_dict = response.to_dict()
    
    generated_content = response_dict['choices'][0]['message']['content']
    
    return generated_content