import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from uploader import upload_video

def get_youtube():
    creds = Credentials(
        None,
        refresh_token=os.getenv("REFRESH_TOKEN"),
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("youtube", "v3", credentials=creds)

if __name__ == "__main__":
    youtube = get_youtube()
    print("YouTube client ready.")

    # Example upload call
    # upload_video(youtube, "video.mp4", "My Title", "My Description", ["tag1", "tag2"])
