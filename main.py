from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje":"arriba las pinches chivas"}