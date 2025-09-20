from fastapi import Request
from fastapi.responses import JSONResponse
from logger import logger

async def catch_exception_middleware(request: Request, call_next):
  try:
    return await call_next(request)
  except Exception as exc:
    logger.exception("Unhandled Exception")
    return JSONResponse(status_code=500 , content={"error":str(exc)})
  
  # this is a custom middleware function for FastAPI that catches unhandled exceptions and returns a JSON error response instead of letting your server crash or return a raw stack trace.