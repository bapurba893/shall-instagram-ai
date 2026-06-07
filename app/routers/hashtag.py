from fastapi import APIRouter
from app.models.schemas import HashtagRequest, HashtagSet
from app.services.openai_service import call_openai
import json

router = APIRouter()

@router.post("/recommend", response_model=HashtagSet)
def recommend_hashtags(request: HashtagRequest):
    system_prompt = (
        "You are an Instagram hashtag strategist. Generate hashtags that maximize reach "
        "by mixing competition levels. Always return valid JSON only, no markdown."
    )
    user_prompt = (
        f"Niche: {request.niche}\n"
        f"Location: {request.location}\n"
        f"Content Type: {request.content_type}\n\n"
        f"Generate Instagram hashtags in 4 buckets:\n"
        f"- high_competition: 5 tags (1M+ posts, broad reach)\n"
        f"- medium_competition: 7 tags (100K-1M posts, targeted)\n"
        f"- low_competition: 7 tags (under 100K posts, niche, easier to rank)\n"
        f"- branded: 3 tags (brand-specific)\n"
        f"- recommended_mix: best 20 tags combined from all buckets\n\n"
        f"Return JSON: {{\"high_competition\": [...], \"medium_competition\": [...], "
        f"\"low_competition\": [...], \"branded\": [...], \"recommended_mix\": [...]}}"
    )

    try:
        ai_response = call_openai(system_prompt, user_prompt, temperature=0.6)
        parsed = json.loads(ai_response)
        return HashtagSet(**parsed)
    except Exception:
        return HashtagSet(
            high_competition=["#fashion", "#style", "#ootd", "#clothing", "#outfit"],
            medium_competition=[
                "#indianfashion", "#d2cfashion", "#fashiontech", "#aifashion",
                "#virtualtryon", "#indiastyle", "#fashionbloggerindia"
            ],
            low_competition=[
                "#kolkatafashion", "#delhifashionblogger", "#mumbaistyle",
                "#collegeoutfitideas", "#shallofficial", "#tryonhaul",
                "#affordablefashionindia"
            ],
            branded=["#Shall", "#ShallFashion", "#ShallTryOn"],
            recommended_mix=[
                "#fashion", "#ootd", "#indianfashion", "#aifashion", "#virtualtryon",
                "#d2cfashion", "#fashiontech", "#style", "#outfit", "#indiastyle",
                "#collegeoutfitideas", "#affordablefashionindia", "#Shall",
                "#ShallFashion", "#ShallTryOn", "#fashionbloggerindia",
                "#clothing", "#shoplook", "#newdrop", "#fashionforward"
            ]
        )
