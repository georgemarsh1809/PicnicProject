from .models import URLObject
from fastapi import Response, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import AnyHttpUrl
from hashids  import Hashids
import json

hashids = Hashids(min_length=6, salt="random_salt")

# Base URL for the shortened URLs
#   This is only used to generate the short URL, which is then returned to the frontend for display purposes only.
#   The frontend will handle the actual redirection to the long URL when the user clicks on the shortened URL, 
#   which parses the code associated to the URL.
BASE_URL = "https://pic.ni/"

def shorten_and_save(newUrl: AnyHttpUrl) -> Response:
    try:
        with open("urlCodes.json", "r") as file:
            url_codes = json.load(file)
    except Exception as e:
        print(f"Error reading URL codes: {e}")

    new_id = 1 # Default ID for the first entry

    # First, check if the URL already exists in the list...
    if url_codes != []: # ...only if the list is not empty
        for code in url_codes: # Iterate through existing codes
            if str(newUrl) == code['longUrl']: # If the URL already exists: 
                # Raise a conflict error
                raise HTTPException(
                    status_code=409,
                    detail=f"Code already exists for this URL: {code['longUrl']}"
                )
            else:
                new_id = url_codes[-1]["id"] + 1  # Increment the last ID, and continue...

    # If the list is empty, we can use the default new_id and create a new entry
    new_code = hashids.encode(new_id) # The code is generated from the new ID using hashids - ensures no duplicate codes
    new_shortUrl = BASE_URL + new_code
    new_entry = jsonable_encoder(URLObject(id=new_id, longUrl=newUrl, shortUrl=new_shortUrl, code=new_code).model_dump(mode="json")) # Create a new URLObject and convert it to a dictionary

    url_codes.append(new_entry)

    # Save the updated list back to the JSON file
    try:
        with open("urlCodes.json", "w") as file:
            json.dump(url_codes, file, indent=4) # Dumps as JSON
            print(f"Successfully added new URL code: {new_entry}")
    except Exception as e:
        print(f"Error writing new URL code: {e}")
    
    return JSONResponse(
    status_code=201,
    content={
        "message": "Shortened URL created successfully",
        "code": str(new_code),
        "short_url": f"http://localhost:8000/{new_code}",
        "original_url": str(newUrl),
    }
)