from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
async def root():   #async lets FastAPI handle many requests concurrently without blocking
  return {"message" : "Hello chatbot"}
