from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from hashids  import Hashids
import json

app = FastAPI() 
hashids = Hashids(min_length=6, salt="random_salt")

class URLObject(BaseModel):
    code: str
    url: str

with open("urlCodes.json", "r") as file:
    url_codes = json.load(file)

@app.get("/{url_code}")
async def get_code(url_code: str):
    for code in url_codes:
        if code['code'] == url_code:
            return RedirectResponse(url=code['url'])
        else:
            return {"error": "URL not found"}

@app.post("/shorten/{url}")
async def shorten_url(url: str):
    return {}


    
