from dataclasses import dataclass
from datetime import datetime
import requests


GRAPH_BASE = "https://graph.facebook.com/v21.0"


@dataclass
class ScheduleResult:
    creation_id: str
    publish_response: dict


class InstagramGraphClient:
    def __init__(self, ig_business_account_id: str, access_token: str) -> None:
        self.ig_business_account_id = ig_business_account_id
        self.access_token = access_token

    def create_scheduled_image_media(
        self,
        image_url: str,
        caption: str,
        publish_time: datetime,
    ) -> str:
        url = f"{GRAPH_BASE}/{self.ig_business_account_id}/media"
        payload = {
            "image_url": image_url,
            "caption": caption,
            "published": "false",
            "scheduled_publish_time": int(publish_time.timestamp()),
            "access_token": self.access_token,
        }

        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()
        return response.json()["id"]

    def publish_media(self, creation_id: str) -> dict:
        url = f"{GRAPH_BASE}/{self.ig_business_account_id}/media_publish"
        payload = {
            "creation_id": creation_id,
            "access_token": self.access_token,
        }

        response = requests.post(url, data=payload, timeout=30)
        response.raise_for_status()
        return response.json()
