import logging
from typing import Dict, Optional
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)


def _build_playlist_body(title: str, description: str, privacy_status: str = "private") -> Dict:
    return {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["playlist", "funnel", "watch next"]
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }


def optimize_playlist_title(channel_name: str, niche: str = "general") -> str:
    return f"{channel_name.title()} {niche.title()} Funnel"


def optimize_playlist_description(channel_name: str, niche: str = "general") -> str:
    return (
        f"Curated {niche} videos from {channel_name.title()} designed to keep viewers engaged. "
        "Subscribe and watch the next video to continue learning."
    )


def get_or_create_playlist(youtube, title: str, description: str, privacy_status: str = "private") -> Optional[str]:
    try:
        request = youtube.playlists().list(part="snippet,status", mine=True, maxResults=50)
        response = request.execute()
        for item in response.get("items", []):
            if item["snippet"]["title"] == title:
                return item["id"]

        playlist_body = _build_playlist_body(title, description, privacy_status)
        created = youtube.playlists().insert(part="snippet,status", body=playlist_body).execute()
        return created.get("id")
    except HttpError as e:
        logger.warning(f"Unable to create or fetch playlist: {e}")
    except Exception as e:
        logger.warning(f"Playlist management skipped: {e}")
    return None


def add_video_to_playlist(youtube, playlist_id: str, video_id: str) -> bool:
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        return True
    except HttpError as e:
        logger.warning(f"Unable to add video to playlist: {e}")
    except Exception as e:
        logger.warning(f"Playlist add skipped: {e}")
    return False


def manage_playlist_for_upload(youtube, video_id: str, channel_name: str, niche: str = "general") -> Optional[str]:
    playlist_title = optimize_playlist_title(channel_name, niche)
    playlist_description = optimize_playlist_description(channel_name, niche)
    playlist_id = get_or_create_playlist(youtube, playlist_title, playlist_description)
    if not playlist_id:
        return None
    add_video_to_playlist(youtube, playlist_id, video_id)
    return playlist_id
