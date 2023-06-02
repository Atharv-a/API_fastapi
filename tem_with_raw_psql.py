from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
import time 
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool= True
    rating:Optional[int]= None

while True:
    try:
        con =psycopg2.connect(host='localhost',database='fastapi',
                            user='postgres',password='data1base',cursor_factory=RealDictCursor)
        cursor=con.cursor()
        print("database connection was succesfull")
        break
    except Exception as error:
        print("connecting to database failed")
        print("error: ",error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""INSERT INTO posts(title,content,published)
                      VALUES(%s,%s,%s) 
                      RETURNING *""",(post.title,post.content,post.published))
    new_post=cursor.fetchone()
    con.commit()
    return{"data":new_post}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * FROM posts 
                      WHERE id = %s""",(str(id)))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts 
                      WHERE id = %s 
                      RETURNING *""",str(id))
    delete_post=cursor.fetchone()
    con.commit()
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'posts with id:{id} does not exits')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    cursor.execute("""UPDATE posts 
                      SET title =%s, content=%s, published=%s 
                      WHERE id = %s
                      RETURNING*""",
                   (post.title, post.content, post.published, str(id)))
    updated_post= cursor.fetchone()
    con.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post wiht id:{id} does not exits')
    return{'data':updated_post}  