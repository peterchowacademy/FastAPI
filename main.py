from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

##making a class for the post and extend to the BaseModel 
##define the sytma for what it should like from the data in frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



# request get Methods url: '/'
'''@ is the python decorator
'app' is the function to call FastAPI() 
'get' is the HTTP request to the API
("/") is the route path for the domain - doesn't make any difference
("/path/vote") then your https should go to this path visist
'''
@app.get("/") #python decorator
# async def root(): # async is when your function take async task such as long time connection for DB
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data" : "this is your posts"}

'''
extract all the fileds from 'Body' and converted to 'python dictionary'
and stored as a variable of 'payload'
'''
@app.post("/posts")
def create_posts(post: Post):
    print(post.rating) #showing one class attribute
    print(post) #this is a pedantic model
    print(post.dict()) #convert the pedantic model to dictionary
    return {"data": post}
    # print(new_post.title)
#title str, content str,
