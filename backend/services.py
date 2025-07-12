import json
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, AnyHttpUrl
from hashids  import Hashids

hashids = Hashids(min_length=6, salt="random_salt")

# Data Models
class URLObject(BaseModel):
    id: int
    code: str
    url: AnyHttpUrl

def shorten_and_save(url: str):
    with open("urlCodes.json", "r") as file:
        url_codes = json.load(file)

    new_id = 1 # Default ID for the first entry

    # First, check if the URL already exists in the list...
    if url_codes != []: # ...only if the list is not empty
        for code in url_codes: # Iterate through existing codes
            if code['url'] == url:
                return Response( content=f"Code already exists for this URL: {code['url']} → /{code['code']}", status_code=409) # If the URL already exists, raise a conflict error
            else:
                new_id = url_codes[-1]["id"] + 1  # Increment the last ID, and continue...

    # If the list is empty, we can use the default new_id and create a new entry
    new_url = url
    new_code = hashids.encode(new_id) # The code is generated from the new ID using hashids - also ensure no duplicates
    new_entry = jsonable_encoder(URLObject(id=new_id, code=new_code, url=new_url).model_dump(mode="json")) # Create a new URLObject and convert it to a dictionary

    url_codes.append(new_entry)

    # Save the updated list back to the JSON file
    with open("urlCodes.json", "w") as file:
        json.dump(url_codes, file, indent=4) # Dumps as JSON
    
    return Response(content=f"Added shortened URL: {new_code}", status_code=201)