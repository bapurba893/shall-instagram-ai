from fastapi import APIRouter
from app.models.schemas import CaptionRequest, CaptionResponse
from app.services.openai_service import call_openai
import json

router = APIRouter()

@router.post("/generate", response_model=CaptionResponse)
def generate_caption(request: CaptionRequest):
    system_prompt = (
        "You are an expert Instagram copywriter for Indian fashion brands. "
        "Write punchy, scroll-stopping captions that convert followers into buyers. "
        "Always return valid JSON only, no markdown, no extra text."
    )

    cta_instruction = (
        "End with a strong CTA like 'Try it on at shall.com' or 'Link in bio to try it on 👆'"
        if request.include_cta else "No call to action needed."
    )

    user_prompt = (
        f"Photo: {request.photo_description}\n"
        f"Target Audience: {request.target_audience}\n"
        f"Tone: {request.tone}\n"
        f"CTA: {cta_instruction}\n\n"
        f"Write an Instagram caption (max 100 words) and suggest 15 hashtags.\n"
        f"Also suggest the best time to post this.\n\n"
        f"Return JSON: {{\"caption\": \"...\", \"hashtags\": [\"#tag1\", ...], "
        f"\"best_posting_time\": \"e.g. 7:30 PM IST\"}}"
    )

    try:
        ai_response = call_openai(system_prompt, user_prompt, temperature=0.85)
        parsed = json.loads(ai_response)
        return CaptionResponse(
            caption=parsed["caption"],
            hashtags=parsed["hashtags"],
            best_posting_time=parsed.get("best_posting_time", "7:30 PM IST")
        )
    except Exception:
        return CaptionResponse(
            caption=(
                "Not just a fit. An experience.\n\n"
                "Try on every piece virtually before you order — get the color, "
                "size, and vibe exactly right. Every time.\n\n"
                "Try it on at shall.com 👆"
            ),
            hashtags=[
                "#shall", "#AIFashion", "#VirtualTryOn", "#IndianFashion",
                "#OOTD", "#FashionTech", "#StyleInspiration", "#D2CFashion",
                "#NewDrop", "#OutfitInspo", "#ShopSmart", "#FashionForward",
                "#GenZFashion", "#TrendyOutfits", "#ShallOfficial"
            ],
            best_posting_time="7:30 PM IST"
        )
