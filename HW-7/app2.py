from datetime import datetime, timezone
from typing import Annotated, List

from annotated_types import MinLen, MaxLen
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field

app = FastAPI(title="Posts & Comments")

# POSTS = [
#     {
#         "id": int,
#         "title": str,
#         "description": str,
#         "created_at": str,
#         "comments": [
#             {
#                 "id": int,
#                 "text": str,
#                 "created_at": str
#             },
#             ....
#         ]
#     },
#     ....
# ]

class Comment(BaseModel):
    id: int
    text: Annotated[str, MinLen(5)]
    created_at: Annotated[datetime, datetime.now(timezone.utc)]

class PostCreate(BaseModel):
    title: Annotated[str, MinLen(5), MaxLen(255)]
    description: Annotated[str, MinLen(5)]

class Post(PostCreate):
    id: int
    created_at: Annotated[datetime, datetime.now(timezone.utc)]
    comments: List[Comment]

NEXT_POST_ID = 1
NEXT_COMMENT_ID = 1
POSTS: List[Post] = [

]


def search_post(post_id: int) -> Post:
    for post in POSTS:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/posts", response_model=List[Post])
def get_posts():
    return POSTS


@app.post("/posts", response_model=Post)
def create_post(data: PostCreate):
    global NEXT_POST_ID
    post = Post(
        id=NEXT_POST_ID,
        comments=[],
        created_at=datetime.now(timezone.utc),
        **data.model_dump()
    )
    POSTS.append(post)
    NEXT_POST_ID += 1
    return post

@app.put("/posts/{post_id}")
def update_post(post_id: int, data: PostCreate, post: PostCreate = Depends(search_post)):
    post["title"] = data.get("title")
    post["description"] = data.get("description")



@app.delete("/posts/{post_id}")
def delete_post(post: Post = Depends(search_post)):
    del_post = post
    POSTS.remove(post)
    return del_post


# создать CRUD для комментариев к постам
#
# GET /posts/{post_id}/comments
# POST /posts/{post_id}/comments
# GET /posts/{post_id}/comments/{comment_id}
# DELETE /posts/{post_id}/comments/{comment_id}
# PUT /posts/{post_id}/comments/{comment_id}