from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from main import bot
bot =  bot()

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def sum(question):
    ans = bot.query(question)
    return {"answer": ans}
