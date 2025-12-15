from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get('/home')
def home():
    return {"This is the home page!"}

text_posts = {
    1: {
    "review_id": 1,
    "rating": 5,
    "title": "Excellent experience",
    "review_text": "The service was fast, friendly, and exceeded my expectations. I would definitely recommend this to others.",
    "reviewer": "Alex M.",
    "date": "2025-01-05"
  },
  2: {
    "review_id": 2,
    "rating": 4,
    "title": "Very good overall",
    "review_text": "Great quality and good value for the price. There is a little room for improvement, but I am satisfied.",
    "reviewer": "Priya K.",
    "date": "2025-01-12"
  },
  3: {
    "review_id": 3,
    "rating": 3,
    "title": "Average experience",
    "review_text": "The product works as described, but nothing really stood out. It was just okay.",
    "reviewer": "Jordan L.",
    "date": "2025-02-01"
  },
  4: {
    "review_id": 4,
    "rating": 2,
    "title": "Disappointing",
    "review_text": "The item arrived late and did not match the description very well. Customer support was slow to respond.",
    "reviewer": "Chen W.",
    "date": "2025-02-10"
  },
  5: {
    "review_id": 5,
    "rating": 1,
    "title": "Very poor",
    "review_text": "Unfortunately, this was a bad experience. The product was defective and I had to request a refund.",
    "reviewer": "Maria S.",
    "date": "2025-02-18"
  }
}


@app.get('/posts')
def get_posts(limit: int = None):

    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.post('/posts/{id}')
def get_post_id(id: int):
    if id not in text_posts:
        raise HTTPException(404, "Review not available")
    return text_posts.get(id)


@app.post('/posts')
def create_post():
    pass