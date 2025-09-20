from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
from routes.upload_pdfs import router as upload_router
from routes.ask_question import router as ask_router

app = FastAPI(title="Medical Assistant API" , description="API for as Medical assistant chatbot")

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_credentials = True,
  allow_methods = ["*"],
  allow_headers = ["*"],
)

# middleware exception handler 
app.middleware("http")(catch_exception_middleware)

#1. upload pdfs 
app.include_router(upload_router)

#2. asking query 
app.include_router(ask_router)