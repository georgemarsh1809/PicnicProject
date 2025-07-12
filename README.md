# URL Shortener API

### Client: Picnic | Job: Junior Backend Engineer

This is my project for the brief provided by Picnic, which was to create a URL
shortener API with the following requirements:

Please build a simple API with:

1. `POST /shorten` – Accepts a long URL, returns a shortened one (e.g.,
   https://pic.ni/abc123)
2. `GET /{code} `– Redirects to the original long URL
3. Basic persistence between requests (e.g., save data to a file or use SQLite)

I built the solution using FastAPI, a Python based API development framework,
for its simplicity and ease of setup and configuration.

The encoded URLs are added to a .json file, each with a unique ID (int), which
is used to generate a unique 6 character code, which can be used in a GET
request to redirect to the original long URL. The long URL to be shortened is
parsed to the `/shorten` endpoint via the request body. Even though this isn't
as practical (can't be simply tested in the URL bar in browser - I use Postman
to test), I decided this over parsing it as a query parameter for a few reasons:

-   There's an inherit URL length limit of 2000 characters for most browsers
-   Parsing as a query param requires careful URL encoding for special
    characters
-   Less secure for sensitive URLs
-   Doeesn't scale well if more params are to be added (expiry time, creation
    date etc.)

Assumptions:

-   This is a test of my ability to interpret requirements and implement an API,
    not of my ability to create a custom hashing algorithm. Considering this, I
    utilised an external hashing module, `hashids.py`, to convert the IDs to
    short, unique codes. In the future, a custom hashing process could be
    implemented for further control and customisation.
