from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



my_posts = [{"title" : "title of the post 1", "Content" : "content of post 1", "id" : 1},
            {"title" : "Favourite Animals", "Content" : "I Like Dog", "id" : 2}
            ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
         return i

#routing
@app.get("/")
#decorator
def get_User():
    return {"Hello": "Sudip"}

@app.get("/posts")
def get_Post():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data" : post}
#title str, content str

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail" : post}

@app.get("/posts/{id}")
def get_post(id: int, response : Response):
    post = find_post(id)
    # if not post:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     return {'message' : f'post with Id {id} was not found'}
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f'Post with ID: {id} was not Found')
    return{"post_detail" : post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    #deleting post
    #find the index in the array that has requried ID
    #my_posts.pop(index)
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesnot found.")

    my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # print(post)
    #find index with the id
    index = find_index_post(id)

    #if the id is not found : 
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {id} doesnot found.")
    
    # updating the post:
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    # return {'message' : 'Update Post'}