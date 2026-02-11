from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    instagram_business_account_id: str
    meta_access_token: str


    @staticmethod
    def from_env() -> "Settings":
        return Settings(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            openai_model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
            instagram_business_account_id=os.environ["INSTAGRAM_BUSINESS_ACCOUNT_ID"],
            meta_access_token=os.environ["META_ACCESS_TOKEN"],
        )
