import time
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models
from . database import engine, get_db

models.Base.metadata.create_all (bind=engine)

app = FastAPI()  #'app' is the instance of this python, which is the FastAPI instance


##making a class for the post and extend to the BaseModel - pydantic model
##define the sytma for what it should like from the data in frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        # conn = psycopg2.connect(host, database, user, password)
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='Password1234', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error )
        time.sleep(2)


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
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}


'''
extract all the fileds from 'Body' and converted to 'python dictionary'
and stored as a variable of 'payload'
'''


@app.post("/posts", status_code=status.HTTP_201_CREATED) #define the decorator
def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # my_posts.append(post_dict)  #append the postID to the post
    # new_post = models.Post(**post.dict())
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}
    # print(new_post.title)
# title str, content str,

@app.get("/posts/{id}") #parathesis refers to the path parameter 
def get_post(id : int, db: Session = Depends(get_db)): #check the if the id is integer, str is string
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post =  db.query(models.Post).filter(models.Post.id == id).first()
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
     
@app.get("/sqlalchemy")
#pass the parameter to the DB as a 'Session' object and depends on the DB
def test_posts (db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #delete the post 
    #find the index in the array that has required ID
    #my_posts.pop(id)
    # cursor.execute ("""DELETE FROM posts WHERE id = % s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post =  db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) #204 when you delete sth, you dont want to send data back

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post_query.first()}


##test newc foldernbbmb