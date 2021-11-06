from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


##making a class for the post and extend to the BaseModel - pydantic model
##define the sytma for what it should like from the data in frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# save the posts in memory (before we set up the database) and state the properties, ID is specific for that particular post
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favouriate food", "content": "I like pizza", "id": 2}]

# request get Methods url: '/'
'''@ is the python decorator
'app' is the function to call FastAPI() 
'get' is the HTTP request to the API
("/") is the route path for the domain - doesn't make any difference
("/path/vote") then your https should go to this path visist
'''


@app.get("/")  # python decorator
# async def root(): # async is when your function take async task such as long time connection for DB
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


'''
extract all the fileds from 'Body' and converted to 'python dictionary'
and stored as a variable of 'payload'
'''


@app.post("/posts")
def create_posts(post: Post):
    # print(post.rating)  # showing one class attribute
    # print(post)  # this is a pedantic model
    # print(post.dict())  # convert the pydantic model to dictionary
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)  #append the postID to the post
    return {"data": post}
    # print(new_post.title)
# title str, content str,



