from pydantic import BaseModel
from typing import List, Optional

# --- Competitor Analysis ---
class CompetitorRequest(BaseModel):
    accounts: List[str]
    your_account: Optional[str] = "shall_official"

class CompetitorInsight(BaseModel):
    account: str
    followers: int
    avg_likes: int
    avg_comments: int
    posts_per_week: int
    top_content_type: str
    top_hashtags: List[str]
    posting_times: List[str]

class CompetitorResponse(BaseModel):
    competitors: List[CompetitorInsight]
    recommendations: List[str]
    ai_summary: str

# --- Content Ideas ---
class ContentRequest(BaseModel):
    business: str
    audience: str
    goal: str
    tone: Optional[str] = "modern and aspirational"

class ContentIdea(BaseModel):
    type: str
    idea: str
    why_it_works: str

class ContentResponse(BaseModel):
    ideas: List[ContentIdea]
    weekly_plan: str

# --- Caption Generator ---
class CaptionRequest(BaseModel):
    photo_description: str
    target_audience: str
    tone: Optional[str] = "Gen Z, cool, minimal"
    include_cta: Optional[bool] = True

class CaptionResponse(BaseModel):
    caption: str
    hashtags: List[str]
    best_posting_time: str

# --- Hashtag Engine ---
class HashtagRequest(BaseModel):
    niche: str
    location: Optional[str] = "India"
    content_type: Optional[str] = "fashion"

class HashtagSet(BaseModel):
    high_competition: List[str]
    medium_competition: List[str]
    low_competition: List[str]
    branded: List[str]
    recommended_mix: List[str]

# --- Posting Time ---
class PostingTimeRequest(BaseModel):
    content_type: str
    target_audience: str
    timezone: Optional[str] = "IST"

class PostingTimeResponse(BaseModel):
    reels: List[str]
    stories: List[str]
    feed_posts: List[str]
    reasoning: str
