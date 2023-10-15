from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """
        Привет мир!
    """
    return {"message": "Hello World"}
