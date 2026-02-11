# AI Influencer Scheduler (MVP)

This project automates a social posting workflow for an AI influencer:

1. Analyze a photo with an LLM vision API.
2. Generate an Instagram caption, hashtags, and a music suggestion.
3. Schedule the post to Instagram at a specific time.

## Important platform note

For Instagram posting, this project uses the **Meta Graph API** (recommended and policy-compliant) for professional accounts. Logging in with browser automation is fragile and can violate platform policies.

Music attachment to feed posts is currently limited in public APIs. This project generates a **music recommendation** so you can apply it in-app where required.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-4.1-mini
INSTAGRAM_BUSINESS_ACCOUNT_ID=...
META_ACCESS_TOKEN=...
```

## Usage

```bash
python main.py \
  --image ./example.jpg \
  --post-time "2026-02-15T18:30:00+00:00" \
  --timezone "UTC"
```

Output includes:
- AI analysis summary
- generated caption
- hashtags
- music recommendation
- scheduled Instagram media creation id + publish response

## Permissions and requirements

- Instagram Professional account connected to a Facebook Page
- `instagram_content_publish` permission in your Meta app
- Long-lived page/user access token with required scopes

## Project structure

- `main.py`: CLI entrypoint
- `src/ai_influencer/ai_writer.py`: photo analysis and copy generation
- `src/ai_influencer/instagram_graph.py`: Graph API scheduling
- `src/ai_influencer/workflow.py`: orchestration

