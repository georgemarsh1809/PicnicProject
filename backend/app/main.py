from .services import shorten_and_save
from .models import URLPayload
from .storage import get_url_by_code
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Create API server
app = FastAPI() 

# Configure CORS to allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Endpoints
@app.get("/")
async def root():
    return {
        "This is the root endpoint. Use /shorten/ to shorten URLs or /{url_code} to access shortened URLs."
    }

@app.get("/{url_code}")
async def get_code(url_code: str):
    # Query the storage layer with the short code provided, to return the long URL for redirect
    response = get_url_by_code(url_code)
    return response

@app.post("/shorten/")
async def shorten_url(payload: URLPayload):
    # If the payload does not contain a valid URL, a RequestValidationError is raised, 
    #   and the exception handler will return a 422 response
    response = shorten_and_save(payload.url)
    return response

# Exception Handling
@app.exception_handler(RequestValidationError)
# This catches any RequestValidationErrors thrown due to an invalid URL format in the payload, 
#   as defined by Pydantic's AnyHttpUrl type
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,  
        content=jsonable_encoder({
            "error": "Invalid URL format, ensure the URL starts with http:// or https://",
        }),
    )
    
