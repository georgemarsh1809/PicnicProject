from .services import shorten_and_save
from .models import URLPayload
from fastapi import FastAPI, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import json

app = FastAPI() 

# Configure CORS to allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Endpoints
@app.get("/")
async def root():
    return {"This is the root endpoint. Use /shorten/ to shorten URLs or /{url_code} to access shortened URLs."}

@app.get("/{url_code}")
async def get_code(url_code: str):
    with open("urlCodes.json", "r") as file:
        url_codes = json.load(file)
    # Redirect to the URL associated with the code, if it exists, otherwise raise a HTTPException
    for code in url_codes:
        if code['code'] == url_code: 
            # Initially was returning a RedirectResponse, but now returning the long URL as JSON so the frontend can handle it
            # return RedirectResponse(url=code['longUrl'], status_code=302)
            return {"longUrl": code["longUrl"]}
    return Response(status_code=404, content="Shortened URL code not found")


@app.post("/shorten/")
async def shorten_url(payload: URLPayload):
    # If the payload does not contain a valid URL, aRequestValidationError is raised, and the exception handler will return a 422 response
    response = shorten_and_save(payload.url)
    return response


# Exception Handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,  
        content=jsonable_encoder({
            "error": "Invalid request body",
            "details": exc.errors()
        }),
    )
    
