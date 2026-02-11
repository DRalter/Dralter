from dataclasses import dataclass
from openai import OpenAI


@dataclass
class GeneratedPost:
    analysis_summary: str
    caption: str
    hashtags: list[str]
    music_suggestion: str


class AIWriter:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_post_from_image_url(self, image_url: str) -> GeneratedPost:
        prompt = (
            "You are helping manage an AI influencer Instagram account. "
            "Analyze the image and produce:\n"
            "1) A 1-2 sentence analysis summary\n"
            "2) A compelling Instagram caption (max 120 words)\n"
            "3) 10 relevant hashtags without # symbols as a JSON array\n"
            "4) One music track recommendation with artist\n"
            "Return strict JSON with keys: analysis_summary, caption, hashtags, music_suggestion."
        )

        response = self.client.responses.create(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": image_url},
                    ],
                }
            ],
            text={"format": {"type": "json_object"}},
        )

        data = response.output[0].content[0].text
        parsed = __import__("json").loads(data)

        return GeneratedPost(
            analysis_summary=parsed["analysis_summary"],
            caption=parsed["caption"],
            hashtags=parsed["hashtags"],
            music_suggestion=parsed["music_suggestion"],
        )
