import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from app.schemas import CreatePost, ReturnPost
from app.db import Post
from datetime import datetime
from app.db import create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
import shutil
import os
from app.images import imagekit
import tempfile


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def home():
    return "This is the home page!"


# upload_file wala function aik 'file parameter' accept kar raha hai jo ke UploadFile type ka hai.
# File(...) ka matlab hai ke yeh parameter zaroori hai aur isay provide karna he hoga jab API endpoint ko call kiya jaye ga.
# caption parameter aik string hai jo ke form data se aayega.
# Form(...) ka matlab hai ke yeh parameter bhi zaroori hai aur isay form data se provide karna hoga.
# 'session' parameter aik AsyncSession type ka hai jo ke get_async_session dependency se aayega.
# Depends(get_async_session) ka matlab hai ke yeh parameter aik dependency injection hai jo ke asynchronous database session provide kare ga.


@app.post("/upload")
async def upload_file(
    user_ki_file: UploadFile = File(...),
    caption: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
):
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(user_ki_file.filename)[1]
        ) as temp_file:

            temp_file_path = temp_file.name
            shutil.copyfileobj(user_ki_file.file, temp_file)

            with open(temp_file_path, "rb") as f:
                upload_result = imagekit.files.upload(
                    file=f.read(),
                    file_name=user_ki_file.filename,
                    use_unique_file_name=True,
                    tags=["backend-upload"],
                )
            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type=(
                    "video"
                    if user_ki_file.content_type.startswith("video/")
                    else "image"
                ),
                file_name=upload_result.name,
                created_at=datetime.now(),
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        user_ki_file.file.close()


@app.get("/feed")
async def get_feed(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat(),
            }
        )
    return {"posts": post_data}


@app.delete("/delete/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)
        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()

        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        await session.delete(post)
        await session.commit()
        return {"success": True, "message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# text_posts = {
#     1: {
#     "rating": 5,
#     "title": "Excellent experience",
#     "review_text": "The service was fast, friendly, and exceeded my expectations. I would definitely recommend this to others.",
#     "reviewer": "Alex M.",
#     "date": "2025-01-05"
#   },
#   2: {
#     "rating": 4,
#     "title": "Very good overall",
#     "review_text": "Great quality and good value for the price. There is a little room for improvement, but I am satisfied.",
#     "reviewer": "Priya K.",
#     "date": "2025-01-12"
#   },
#   3: {
#     "rating": 3,
#     "title": "Average experience",
#     "review_text": "The product works as described, but nothing really stood out. It was just okay.",
#     "reviewer": "Jordan L.",
#     "date": "2025-02-01"
#   },
#   4: {
#     "rating": 2,
#     "title": "Disappointing",
#     "review_text": "The item arrived late and did not match the description very well. Customer support was slow to respond.",
#     "reviewer": "Chen W.",
#     "date": "2025-02-10"
#   },
#   5: {
#     "rating": 1,
#     "title": "Very poor",
#     "review_text": "Unfortunately, this was a bad experience. The product was defective and I had to request a refund.",
#     "reviewer": "Maria S.",
#     "date": "2025-02-18"
#   }
# }

# @app.get('/posts')
# def get_posts(limit: int = None):

#     if limit:
#         return list(text_posts.values())[:limit]
#     return text_posts


# @app.post('/posts/{id}')
# def get_post_id(id: int) -> ReturnPost:
#     if id not in text_posts:
#         raise HTTPException(404, "Review not available")
#     return text_posts.get(id)


# @app.post('/posts')
# def create_post(post: CreatePost) -> ReturnPost:
#   new_post = {'rating': post.rating, 'review_text': post.review_text, 'reviewer': post.reviewer, 'title': post.title, 'date': post.date}
#   text_posts[max(text_posts) + 1] = new_post
#   return new_post
