from dataclasses import dataclass
from datetime import datetime

from .ai_writer import AIWriter, GeneratedPost
from .instagram_graph import InstagramGraphClient, ScheduleResult


@dataclass
class WorkflowOutput:
    generated_post: GeneratedPost
    schedule_result: ScheduleResult


class InfluencerWorkflow:
    def __init__(self, writer: AIWriter, instagram_client: InstagramGraphClient) -> None:
        self.writer = writer
        self.instagram_client = instagram_client

    def run(self, image_url: str, publish_time: datetime) -> WorkflowOutput:
        generated = self.writer.generate_post_from_image_url(image_url)
        hashtags = " ".join(f"#{tag.strip().lstrip('#')}" for tag in generated.hashtags)
        final_caption = (
            f"{generated.caption}\n\n"
            f"{hashtags}\n\n"
            f"🎵 Music idea: {generated.music_suggestion}"
        )

        creation_id = self.instagram_client.create_scheduled_image_media(
            image_url=image_url,
            caption=final_caption,
            publish_time=publish_time,
        )
        publish_response = self.instagram_client.publish_media(creation_id)

        return WorkflowOutput(
            generated_post=generated,
            schedule_result=ScheduleResult(
                creation_id=creation_id,
                publish_response=publish_response,
            ),
        )
