from fastapi import APIRouter
from app.models.schemas import ContentRequest, ContentResponse, ContentIdea
from app.services.openai_service import call_openai
import json

router = APIRouter()

@router.post("/ideas", response_model=ContentResponse)
def generate_content_ideas(request: ContentRequest):
    system_prompt = (
        "You are a top Instagram content strategist specializing in Indian D2C fashion brands. "
        "Generate highly specific, creative, and viral-worthy content ideas. "
        "Always return valid JSON only, no markdown, no extra text."
    )
    user_prompt = (
        f"Brand: {request.business}\n"
        f"Target Audience: {request.audience}\n"
        f"Goal: {request.goal}\n"
        f"Tone: {request.tone}\n\n"
        f"Generate 8 Instagram content ideas covering: Reel, Carousel, Story, Meme, "
        f"Behind-the-Scenes, UGC, Educational, Product Showcase.\n\n"
        f"Return JSON: {{\"ideas\": ["
        f"{{\"type\": \"Reel\", \"idea\": \"...\", \"why_it_works\": \"...\"}},"
        f" ...], \"weekly_plan\": \"short 3-sentence weekly posting plan\"}}"
    )

    try:
        ai_response = call_openai(system_prompt, user_prompt, temperature=0.8)
        parsed = json.loads(ai_response)
        ideas = [ContentIdea(**i) for i in parsed.get("ideas", [])]
        weekly_plan = parsed.get("weekly_plan", "")
    except Exception:
        ideas = [
            ContentIdea(type="Reel", idea="5 Ways To Style One Kurta For Different Occasions",
                       why_it_works="High shareability, saves, and targets styling curiosity"),
            ContentIdea(type="Carousel", idea="Summer Outfit Guide: What To Wear In 40°C Heat",
                       why_it_works="Seasonal relevance drives saves and shares"),
            ContentIdea(type="Story", idea="Poll: Which color hoodie should we drop next?",
                       why_it_works="Interactive content boosts story views and engagement"),
            ContentIdea(type="Meme", idea="POV: You used Shall AI and now you can't stop trying outfits",
                       why_it_works="Relatable memes drive comments and shares among Gen Z"),
            ContentIdea(type="Behind-the-Scenes", idea="How our AI actually figures out your perfect size",
                       why_it_works="Tech transparency builds trust and curiosity"),
            ContentIdea(type="UGC", idea="Repost a customer's try-on result with their reaction",
                       why_it_works="Social proof is the strongest purchase trigger"),
            ContentIdea(type="Educational", idea="3 mistakes people make when buying clothes online (and how AI fixes them)",
                       why_it_works="Pain-point content gets saved and shared widely"),
            ContentIdea(type="Product Showcase", idea="New Drop: The outfit that sold out in 2 hours last time",
                       why_it_works="FOMO drives immediate traffic and sales"),
        ]
        weekly_plan = (
            "Mon & Thu: Post Reels (try-on demos or styling tips). "
            "Wed: Carousel or educational post. "
            "Daily: 4-5 Stories mixing polls, countdowns, and behind-the-scenes. "
            "Sat: UGC repost or customer feature."
        )

    return ContentResponse(ideas=ideas, weekly_plan=weekly_plan)
