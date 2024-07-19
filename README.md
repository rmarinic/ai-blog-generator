# AI Blog Post Generator from YouTube Link

This project is a Python Django-based web application that generates comprehensive blog articles from YouTube video transcripts. By leveraging various powerful libraries and APIs such as PyTube, AssemblyAI, and AI21, this tool extracts audio from YouTube videos, transcribes it, and generates well-formatted blog posts. The application runs on a PostgreSQL database in the background to ensure robust data handling and storage.

## Features

- **YouTube Video to Blog Post**: Converts YouTube video content into a written blog article.
- **Automatic Transcription**: Uses AssemblyAI to transcribe the audio content of YouTube videos.
- **AI-Powered Blog Generation**: Utilizes AI21’s language model to create a structured and readable blog post from the transcript.
- **User-Friendly Interface**: Simple and intuitive web interface for users to input YouTube links and get blog content.

## Libraries and Tools Used

- **Django**: The high-level Python Web framework used to build the web application.
- **PyTube**: A lightweight, dependency-free Python library used to download YouTube videos.
- **AssemblyAI**: An API service for automatic speech recognition (ASR) used to transcribe YouTube video audio.
- **AI21**: An advanced language model API used to generate human-like text and create the blog post from the transcription.
- **PostgreSQL**: A powerful, open-source object-relational database system used to handle and store data in the background.
