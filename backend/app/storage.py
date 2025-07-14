from fastapi import Response, HTTPException
from fastapi.responses import JSONResponse
import json

def open_JSON_file():
    # Try opening the JSON file: 
    #   if it fails, a SystemError is thrown so the app doesn't continue
    try:
        with open("urlCodes.json", "r") as file:
            return json.load(file)
    except Exception as e:
        raise SystemError(f"Error reading URL codes: {e}")

def get_url_by_code(url_code: str):
    # Try opening the JSON file: 
    try:
        with open("urlCodes.json", "r") as file:
            url_codes = json.load(file)
    except Exception as e:
        raise SystemError(f"Error reading URL codes: {e}")

    # Search the url_codes array for the parsed short code
    for code in url_codes:
        if code['code'] == url_code: 
            return JSONResponse(status_code=200, content={"longUrl": code["longUrl"]} )

    raise HTTPException(status_code=404, detail="Shortened URL code not found")

def save_url_code(url_codes: list) -> Response:
    # Try saving the new list of url_codes, which contains the new URLObject
    try:
        with open("urlCodes.json", "r+") as file:
            json.dump(url_codes, file, indent=4)
    except Exception as e:
        print(f"Error writing URL codes: {e}")
        return Response(status_code=500, content="Error saving URL codes")

    # If successful, return a 201 Created response
    return Response(status_code=201, content="Shortened URL created successfully")