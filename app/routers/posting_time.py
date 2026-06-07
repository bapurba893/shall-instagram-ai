from fastapi import APIRouter
from app.models.schemas import PostingTimeRequest, PostingTimeResponse
from app.mock_data.instagram_data import MOCK_ENGAGEMENT_DATA
from app.services.openai_service import call_openai
import json

router = APIRouter()

@router.post("/predict", response_model=PostingTimeResponse)
def predict_posting_time(request: PostingTimeRequest):
    audience_key = "general"
    audience_lower = request.target_audience.lower()
    if "college" in audience_lower or "student" in audience_lower:
        audience_key = "college_students"
    elif "professional" in audience_lower or "working" in audience_lower:
        audience_key = "working_professionals"

    engagement_data = MOCK_ENGAGEMENT_DATA[audience_key]

    system_prompt = (
        "You are an Instagram analytics expert. Predict the best posting times based on "
        "audience behavior data. Always return valid JSON only, no markdown."
    )
    user_prompt = (
        f"Content type: {request.content_type}\n"
        f"Target audience: {request.target_audience}\n"
        f"Timezone: {request.timezone}\n"
        f"Engagement data: {json.dumps(engagement_data)}\n\n"
        f"Predict the 3 best times for:\n"
        f"- reels (when people browse and share)\n"
        f"- stories (when people are casually scrolling)\n"
        f"- feed_posts (when people are focused and engage deeply)\n\n"
        f"Also provide a short reasoning (2 sentences).\n"
        f"Return JSON: {{\"reels\": [...], \"stories\": [...], "
        f"\"feed_posts\": [...], \"reasoning\": \"...\"}}"
    )

    try:
        ai_response = call_openai(system_prompt, user_prompt, temperature=0.5)
        parsed = json.loads(ai_response)
        return PostingTimeResponse(**parsed)
    except Exception:
        return PostingTimeResponse(
            reels=["7:30 PM IST", "9:00 PM IST", "12:00 PM IST"],
            stories=["1:00 PM IST", "6:00 PM IST", "10:00 PM IST"],
            feed_posts=["8:00 PM IST", "7:00 PM IST", "11:00 AM IST"],
            reasoning=(
                f"For {request.target_audience}, Instagram usage peaks in the evening after "
                f"work/college hours (7-10 PM IST) and during lunch breaks (12-1 PM IST). "
                f"Reels get the most reach when posted before peak hours so the algorithm "
                f"can amplify them right as traffic spikes."
            )
        )
