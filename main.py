import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from src.ai_influencer.ai_writer import AIWriter
from src.ai_influencer.config import Settings
from src.ai_influencer.instagram_graph import InstagramGraphClient
from src.ai_influencer.workflow import InfluencerWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="AI Influencer Instagram Scheduler")
    parser.add_argument("--image", required=True, help="Public image URL")
    parser.add_argument(
        "--post-time",
        required=True,
        help="Publish time in ISO format, e.g. 2026-02-15T18:30:00+00:00",
    )
    parser.add_argument("--timezone", default="UTC", help="Timezone name, e.g. UTC")
    return parser


def main() -> None:
    load_dotenv()
    args = build_parser().parse_args()

    local_time = datetime.fromisoformat(args.post_time)
    publish_time = local_time.astimezone(ZoneInfo(args.timezone))

    settings = Settings.from_env()
    writer = AIWriter(api_key=settings.openai_api_key, model=settings.openai_model)
    ig_client = InstagramGraphClient(
        ig_business_account_id=settings.instagram_business_account_id,
        access_token=settings.meta_access_token,
    )
    workflow = InfluencerWorkflow(writer=writer, instagram_client=ig_client)

    result = workflow.run(image_url=args.image, publish_time=publish_time)

    print("Analysis:", result.generated_post.analysis_summary)
    print("Caption:", result.generated_post.caption)
    print("Hashtags:", ", ".join(result.generated_post.hashtags))
    print("Music suggestion:", result.generated_post.music_suggestion)
    print("Creation ID:", result.schedule_result.creation_id)
    print("Publish response:", result.schedule_result.publish_response)


if __name__ == "__main__":
    main()
