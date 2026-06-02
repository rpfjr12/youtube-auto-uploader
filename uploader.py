import os
import time
from googleapiclient.http import MediaFileUpload
from logger import log_line

UPLOAD_TIMEOUT_SECONDS = 3600  # 1 hour max per upload

def upload_video(youtube, file_path, title, description, tags):
    """
    Upload a video to YouTube with timeout protection.
    
    Args:
        youtube: Authenticated YouTube API client
        file_path: Path to video file
        title: Video title
        description: Video description
        tags: List of tags
    
    Returns:
        Video ID on success
        
    Raises:
        TimeoutError: If upload exceeds timeout
        Exception: If upload fails
    """
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags
        },
        "status": {
            "privacyStatus": "private"
        }
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    start_time = time.time()
    chunk_count = 0
    last_progress = 0
    
    while response is None:
        # Check timeout
        elapsed = time.time() - start_time
        if elapsed > UPLOAD_TIMEOUT_SECONDS:
            raise TimeoutError(f"Upload exceeded {UPLOAD_TIMEOUT_SECONDS}s timeout after {chunk_count} chunks")
        
        try:
            status, response = request.next_chunk()
            chunk_count += 1
            
            if status:
                progress = int(status.progress() * 100)
                if progress != last_progress and progress % 10 == 0:
                    log_line(f"Upload progress: {progress}%")
                    last_progress = progress
        except Exception as e:
            log_line(f"WARNING: Upload error, retrying: {e}")
            time.sleep(2)
            # Continue loop to retry

    log_line(f"Upload complete: {response['id']} ({chunk_count} chunks in {elapsed:.1f}s)")
    return response["id"]
