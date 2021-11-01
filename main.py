from fastapi import FastAPI

app = FastAPI()

'''@ is the python decorator
app is the function to call FastAPI() 
get is the HTTP request to the API
("/") is the route path for the domain - doesn't make any difference
("/path/vote") then your https should go to this path visist
'''
@app.get("/") #python decorator
# async def root(): # async is when your function take async task such as long time connection for DB
def root():
    return {"message": "Hello World"}