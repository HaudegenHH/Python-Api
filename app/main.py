from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):  # extends BaseModel
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None  # defaults to None/NULL


my_posts = [{"id": 1, "title": "title of post1", "content": "content of post1"},
            {"id": 2, "title": "title of post2", "content": "content of post2"},
            {"id": 3, "title": "title of post3", "content": "content of post3"}]


def find_by(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_from_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():  # converts id automatically into integer
    post = my_posts[len(my_posts)-1]
    return {"latest_Post": post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_by(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with the id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id: {id} was not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    # print(post)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_from_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # print(post)
    index = find_index_from_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with the id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
