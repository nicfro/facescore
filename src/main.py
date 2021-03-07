import os
import sys
sys.path.insert(0, os.getcwd())

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.endpoints import docs, users, login, vote, image
from src.utils.common_logger import logger


# Create API Application
app = FastAPI()


# Global error handler
@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    logger.error(base_error_message)
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}", "detail": f"{err}"})

# Add endpoints
app.include_router(docs.router)
app.include_router(users.router)
app.include_router(login.router)
app.include_router(vote.router)
app.include_router(image.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
