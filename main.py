from fastapi import FastAPI, Response, status, HTTPException
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

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

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


@app.post("/posts") #define the decorator
def create_posts(post: Post, status_code=status.HTTP_201_CREATED):
    # print(post.rating)  # showing one class attribute
    # print(post)  # this is a pedantic model
    # print(post.dict())  # convert the pydantic model to dictionary
    post_dict = post.dict()
    post_dict["id"] = randrange(0,1000000)
    my_posts.append(post_dict)  #append the postID to the post
    return {"data": post}
    # print(new_post.title)
# title str, content str,

@app.get("/posts/{id}") #parathesis refers to the path parameter 
def get_post(id : int): #check the if the id is integer, str is string
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")
        '''
        #this is before use of def get_post(id : int, response : Response), 
        # and marked the response:Response in def
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message' : f"post with id {id} was not found"}
        '''
    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id):
    #delete the post 
    #find the index in the array that has required ID
    #my_posts.pop(id)
    index = find_index_post(id)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #204 when you delete sth, you dont want to send data back