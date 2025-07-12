from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, AnyHttpUrl
import json
from services import *

app = FastAPI() 

# Data Models
class URLPayload(BaseModel):
    url: AnyHttpUrl

with open("urlCodes.json", "r") as file:
    url_codes = json.load(file)

# Endpoints
@app.get("/")
async def root():
    return {"This is the root endpoint. Use /shorten/ to shorten URLs or /{url_code} to access shortened URLs."}

@app.get("/{url_code}")
async def get_code(url_code: str):
    # Redirect to the URL associated with the code, if it exists, otherwise raise a HTTPException
    for code in url_codes:
        if code['code'] == url_code:
            return RedirectResponse(url=code['url'], status_code=302)
    return Response(status_code=404, content="Shortened URL code not found")


@app.post("/shorten/")
async def shorten_url(payload: URLPayload):
    # If the payload does not contain a valid URL, aRequestValidationError is raised, and the exception handler will return a 422 response
    response = shorten_and_save(payload.url)
    return response


# Exception Handling
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc: RequestValidationError):
    return JSONResponse(
        status_code=422,  
        content=jsonable_encoder({
            "error": "Invalid request body",
            "details": exc.errors()
        }),
    )
    
