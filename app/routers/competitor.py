from fastapi import APIRouter
from app.models.schemas import CompetitorRequest, CompetitorResponse, CompetitorInsight
from app.mock_data.instagram_data import MOCK_COMPETITOR_DATA
from app.services.openai_service import call_openai
import json

router = APIRouter()


def estimate_brand_profile(account: str) -> dict:
    """
    For any unknown brand, ask GPT to estimate realistic Instagram metrics
    based on the brand name and fashion industry context.
    """
    system_prompt = (
        "You are a social media analyst with deep knowledge of fashion brands on Instagram. "
        "When given a brand name, estimate its realistic Instagram metrics based on its "
        "known market size, region, and category. Always return valid JSON only, no markdown."
    )
    user_prompt = (
        f"Estimate realistic Instagram metrics for the fashion brand: '{account}'\n\n"
        f"Consider: Is it Indian or global? Luxury or affordable? Mass market or niche?\n\n"
        f"Return JSON with exactly these fields:\n"
        f"{{\n"
        f"  \"followers\": <integer>,\n"
        f"  \"avg_likes\": <integer>,\n"
        f"  \"avg_comments\": <integer>,\n"
        f"  \"posts_per_week\": <integer between 1-10>,\n"
        f"  \"top_content_type\": \"<string, e.g. Reels, Carousels, Stories>\",\n"
        f"  \"top_hashtags\": [\"#tag1\", \"#tag2\", \"#tag3\", \"#tag4\", \"#tag5\"],\n"
        f"  \"posting_times\": [\"<time IST>\", \"<time IST>\"]\n"
        f"}}"
    )

    try:
        ai_response = call_openai(system_prompt, user_prompt, temperature=0.3)
        estimated = json.loads(ai_response)
        # Validate all required fields are present
        required = ["followers", "avg_likes", "avg_comments", "posts_per_week",
                    "top_content_type", "top_hashtags", "posting_times"]
        if all(k in estimated for k in required):
            return estimated
    except Exception:
        pass

    # Hard fallback if GPT estimation also fails
    return MOCK_COMPETITOR_DATA["default"]


@router.post("/analyze", response_model=CompetitorResponse)
def analyze_competitors(request: CompetitorRequest):
    competitors = []

    for account in request.accounts:
        key = account.lower().replace("@", "").replace("_official", "").strip()

        if key in MOCK_COMPETITOR_DATA:
            # Known brand — use precise mock data instantly
            data = MOCK_COMPETITOR_DATA[key]
        else:
            # Unknown brand — ask GPT to estimate realistic metrics
            data = estimate_brand_profile(account)

        competitors.append(CompetitorInsight(account=account, **data))

    competitor_summary = "\n".join([
        f"- {c.account}: {c.followers:,} followers, {c.avg_likes:,} avg likes, "
        f"{c.posts_per_week} posts/week, top content: {c.top_content_type}, "
        f"posts at {', '.join(c.posting_times)}"
        for c in competitors
    ])

    system_prompt = (
        "You are an expert Instagram growth strategist for fashion brands in India. "
        "Analyze competitor data and give sharp, actionable recommendations."
    )
    user_prompt = (
        f"Our brand is Shall — an AI-powered fashion try-on startup targeting young Indians.\n\n"
        f"Competitor data:\n{competitor_summary}\n\n"
        f"Give:\n"
        f"1. A concise AI summary (3-4 sentences) of what competitors are doing well\n"
        f"2. Exactly 5 specific recommendations for Shall to outperform them\n"
        f"Format as JSON: {{\"summary\": \"...\", \"recommendations\": [\"...\", ...]}}"
    )

    try:
        ai_response = call_openai(system_prompt, user_prompt)
        parsed = json.loads(ai_response)
        summary = parsed.get("summary", "Analysis complete.")
        recommendations = parsed.get("recommendations", [])
    except Exception:
        summary = "Competitor analysis complete. Use the data above to refine your strategy."
        recommendations = [
            "Increase reel frequency to match top competitors (5-7/week)",
            "Post consistently during 7-9 PM IST for maximum reach",
            "Use a mix of branded + niche hashtags (20-25 per post)",
            "Leverage your AI try-on feature as a unique content angle",
            "Engage with followers within the first 30 minutes of posting"
        ]

    return CompetitorResponse(
        competitors=competitors,
        recommendations=recommendations,
        ai_summary=summary
    )
