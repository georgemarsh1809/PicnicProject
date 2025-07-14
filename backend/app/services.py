from .models import URLObject
from .storage import save_url_code, open_JSON_file
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import AnyHttpUrl
from hashids  import Hashids
from dotenv import load_dotenv
import os

load_dotenv()
SALT = os.getenv("SALT", "fallback-s9kcL-salt")
hashids = Hashids(min_length=6, salt=SALT)

# Base URL for the shortened URLs:
BASE_URL = "https://pic.ni/"
# This is only used to generate the short URL, which is stored in the JSON and then returned to the frontend 
#   for display purposes only.
# The frontend will handle the actual redirection to the long URL when the user clicks on the short URL button, 

def shorten_and_save(newUrl: AnyHttpUrl) -> Response:
    # Open the JSON 
    url_codes = open_JSON_file()

    # Default ID for the first entry
    new_id = 1 

    # Only if the JSON is not empty (i.e. there are codes stored)...
    if url_codes: 
        # First, check if the URL already exists in the list...
        # Iterate through existing codes:
        for code in url_codes: 
            # If the URL already exists: 
            if str(newUrl) == code['longUrl']: 
                # Raise a `409 Conflict` error as a JSON response so that React can render the error message
                return JSONResponse(
                    status_code=409,
                    content=jsonable_encoder({
                        "error": f"Code already exists for this URL: {code['longUrl']}",
                    }),
                )
            else:
                # If it doesn't already exist, create a new_id by incrementing the last ID stored, and continue...
                new_id = url_codes[-1]["id"] + 1  

    # If the list is empty, we can use the default new_id of 1 and create a new entry using the URLObject data model
    # The code is generated from the new ID using hashids - this ensures no duplicate codes since each ID is incremented and unique
    new_code = hashids.encode(new_id) 
    new_shortUrl = BASE_URL + new_code
    # Create a new URLObject and convert it to a dictionary
    new_entry = jsonable_encoder(URLObject(id=new_id, longUrl=newUrl, shortUrl=new_shortUrl, code=new_code).model_dump(mode="json")) 

    url_codes.append(new_entry)

    # Save the updated list back to the JSON file
    response = save_url_code(url_codes)
    return response


    
