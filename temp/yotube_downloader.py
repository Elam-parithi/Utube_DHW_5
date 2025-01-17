import youtube_dl

def download_youtube_video(video_url):
    try:
        # Set up youtube-dl options
        ydl_opts = {
            'format': 'best',  # Download the best available quality
            'outtmpl': '%(title)s.%(ext)s',  # Save as video title
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading...")
            ydl.download([video_url])
            print("Download complete! File saved in the current directory.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    # Input the YouTube video URL
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)
