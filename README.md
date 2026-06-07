# Shall Instagram AI Growth Assistant

AI-powered Instagram growth tool for **Shall** — an Indian AI fashion try-on startup.  
Built with FastAPI + OpenAI GPT-4o-mini. Deployable via Docker and AWS EC2.

---

## Features

| # | Feature | Endpoint |
|---|---------|----------|
| 1 | Competitor Analysis Agent | `POST /competitor/analyze` |
| 2 | Content Idea Generator | `POST /content/ideas` |
| 3 | Caption Generator | `POST /caption/generate` |
| 4 | Hashtag Recommendation Engine | `POST /hashtags/recommend` |
| 5 | Best Posting Time Predictor | `POST /posting-time/predict` |

---

## Project Structure

```
shall-instagram-ai/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── models/
│   │   └── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── competitor.py        # Competitor analysis
│   │   ├── content.py           # Content ideas
│   │   ├── caption.py           # Caption generator
│   │   ├── hashtag.py           # Hashtag engine
│   │   └── posting_time.py      # Posting time predictor
│   ├── services/
│   │   └── openai_service.py    # OpenAI GPT-4o-mini wrapper
│   └── mock_data/
│       └── instagram_data.py    # Mock competitor & engagement data
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Local Setup

### 1. Clone & configure

```bash
git clone https://github.com/YOUR_USERNAME/shall-instagram-ai.git
cd shall-instagram-ai

cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

### 2. Run with Docker Compose (recommended)

```bash
docker-compose up --build
```

App runs at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

### 3. Run locally (without Docker)

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## API Usage Examples

### Competitor Analysis
```bash
curl -X POST http://localhost:8000/competitor/analyze \
  -H "Content-Type: application/json" \
  -d '{"accounts": ["myntra", "ajio", "zara"], "your_account": "shall_official"}'
```

### Content Ideas
```bash
curl -X POST http://localhost:8000/content/ideas \
  -H "Content-Type: application/json" \
  -d '{"business": "AI Fashion Brand", "audience": "College Students", "goal": "Increase Followers", "tone": "modern and fun"}'
```

### Caption Generator
```bash
curl -X POST http://localhost:8000/caption/generate \
  -H "Content-Type: application/json" \
  -d '{"photo_description": "Black hoodie flatlay", "target_audience": "Gen Z India", "tone": "cool, minimal", "include_cta": true}'
```

### Hashtag Recommendations
```bash
curl -X POST http://localhost:8000/hashtags/recommend \
  -H "Content-Type: application/json" \
  -d '{"niche": "AI fashion try-on", "location": "India", "content_type": "Reels"}'
```

### Posting Time Predictor
```bash
curl -X POST http://localhost:8000/posting-time/predict \
  -H "Content-Type: application/json" \
  -d '{"content_type": "Reel", "target_audience": "College Students", "timezone": "IST"}'
```

---

## Docker Hub — Push & Pull

### Build and push to Docker Hub

```bash
# 1. Login to Docker Hub
docker login

# 2. Build the image
docker build -t YOUR_DOCKERHUB_USERNAME/shall-instagram-ai:latest .

# 3. Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/shall-instagram-ai:latest
```

### Your marketing team pulls and runs it

```bash
# Pull from Docker Hub
docker pull YOUR_DOCKERHUB_USERNAME/shall-instagram-ai:latest

# Run with your API key
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key-here \
  --name shall-instagram-ai \
  YOUR_DOCKERHUB_USERNAME/shall-instagram-ai:latest
```

---

## AWS EC2 Deployment

### Step 1: Launch EC2 instance
- Go to AWS Console → EC2 → Launch Instance
- Choose: **Ubuntu 22.04 LTS**
- Instance type: **t2.micro** (free tier) or t3.small for production
- Security group: Allow inbound **port 8000** and **port 22** (SSH)
- Download your `.pem` key file

### Step 2: SSH into your instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

### Step 3: Install Docker on EC2

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu
# Log out and back in for group change to take effect
```

### Step 4: Pull and run your app

```bash
docker pull YOUR_DOCKERHUB_USERNAME/shall-instagram-ai:latest

docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key-here \
  --restart always \
  --name shall-instagram-ai \
  YOUR_DOCKERHUB_USERNAME/shall-instagram-ai:latest
```

### Step 5: Access the app

```
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

Share this URL with your marketing team — they can use the interactive Swagger UI directly.

### (Optional) Step 6: Add a domain + HTTPS

Use **Nginx** as a reverse proxy and **Certbot** for free SSL:

```bash
sudo apt install nginx certbot python3-certbot-nginx -y

# Configure nginx to proxy port 80 → 8000
sudo nano /etc/nginx/sites-available/shall

# Add:
# server {
#     listen 80;
#     server_name yourdomain.com;
#     location / { proxy_pass http://localhost:8000; }
# }

sudo ln -s /etc/nginx/sites-available/shall /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Upgrading from Mock Data to Real Instagram Data

When ready to use real Instagram data, replace mock data with RapidAPI:

```python
# In app/services/openai_service.py, add:
import httpx

async def fetch_instagram_data(username: str, rapidapi_key: str):
    url = "https://instagram-scraper-api2.p.rapidapi.com/v1/info"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "instagram-scraper-api2.p.rapidapi.com"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params={"username_or_id_or_url": username})
        return response.json()
```

Add `RAPIDAPI_KEY=your-key` to `.env` and swap out mock data calls.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `RAPIDAPI_KEY` | No (future) | RapidAPI key for real Instagram data |

---

## Cost Estimate

| Service | Cost |
|---------|------|
| AWS EC2 t2.micro | Free (12 months) |
| OpenAI GPT-4o-mini | ~₹0.04 per request |
| Docker Hub | Free (public repo) |
| **Total for 1000 requests/month** | **~₹40/month** |
