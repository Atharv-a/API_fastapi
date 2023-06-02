from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

# import psycopg2
# import time 
# from psycopg2.extras import RealDictCursor

# while True:
#     try:
#         con =psycopg2.connect(host='localhost',database='fastapi',
#                             user='postgres',password='data1base',cursor_factory=RealDictCursor)
#         cursor=con.cursor()
#         print("database connection was succesfull")
#         break
#     except Exception as error:
#         print("connecting to database failed")
#         print("error: ",error)
#         time.sleep(2)
