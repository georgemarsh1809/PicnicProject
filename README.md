# URL Shortener API

![Alt text](/frontend/public/picnicproj.png 'screenshot')

### Client: Picnic | Job: Junior Backend Engineer

This is my project for the brief provided by Picnic, which was to create a URL
shortener API with the following requirements:

#### 📋 Requirements :

-   Please build a simple API with:

1. `POST /shorten` – Accepts a long URL, returns a shortened one (e.g.,
   https://pic.ni/abc123)
2. `GET /{code} `– Redirects to the original long URL
3. Basic persistence between requests (e.g., save data to a file or use SQLite)

#### 🛠️ Tech:

-   I built the solution using FastAPI, a Python based API development
    framework, for its simplicity and ease of setup and configuration.
-   I also built a simple UI using React for its easy implementation, and to
    highlight my proficiency with JavaScript/HTML/CSS.

#### 📜 Assumptions:

-   This is a test of my ability to interpret requirements and implement an API,
    not of my ability to create a custom hashing algorithm. Considering this, I
    utilised an external hashing module, `hashids.py`, to convert the IDs to
    short, unique codes. In the future, a custom hashing process could be
    implemented for further control and customisation.

-   The base URL doesn't necessarily impact the integrity of the solution: it's
    displayed as https://pic.ni/{code} for consistency with the requirements,
    but its only the code which is relevant. Of course, when hosted locally, the
    base URL is `https://localhost:8000`, but in production, this could be set
    to anything.

#### 📊 Data Storage

-   The stored URLs are added to a .json file, each with a unique ID (int),
    which is used to generate a unique 6 character code, which can be used in a
    GET request to redirect to the original long URL. The long URL to be
    shortened is parsed to the `/shorten` endpoint via the request body. Even
    though this isn't as practical (can't be simply tested in the URL bar in
    browser - I use Postman to test), I decided this over parsing it as a query
    parameter for a few reasons:

    -   There's an inherit URL length limit of 2000 characters for most browsers
    -   Parsing as a query param requires careful URL encoding for special
        characters
    -   Less secure for sensitive URLs
    -   Doesn't scale well if more params are to be added (expiry time, creation
        date etc.)

#### ⚠️ Interesting Problems I Faced With This Project:

-   At one point, I was having an interesting issue of duplicate URLs being
    added. I was sure that the problem was to do with the comparison statement
    in `services.py`, where the incoming `newUrl` was being compared to each url
    in the JSON store: `if newUrl == code['url']`. My intuition was telling me
    that the issue was related to the Type of each operand being different. To
    debug: After some printing of Types and values, I could see the values were
    the same, but the types were different. The URL from the JSON store,
    `code['url']`, is a string, but incoming `newUrl`, as defined in the
    function arguments, is of type `AnyHttpUrl`. I did some research, and found
    out that when these are compared, even when the values are the same, it can
    return false. I resolved this by wrapping the incoming data with the `str()`
    method; `str(newUrl)`. This immediately solved the problem and dupes were
    not being added.

-   After initially implementing the Frontend and the `POST` API call to add a
    new URL, even with static data (e.g. "https://example.com") as the body of
    the request, I was getting a CORS error, which was throwing a HTTP response
    of `422 Unprocessable Content`. This confused me since I had just explicitly
    implemented the Type of the payload to be of `AnyHttpUrl` from Pydantic, to
    ensure that the format of the URL was valid. I was also slightly concerned
    since I know how much of a pain CORS errors are to fix. To debug, I did some
    research to ensure the structure of the body for `POST` requests in React
    (JavaScript) was correct → It was here I learned that you have to include a
    request header of `{ 'Content-Type': 'application/json', }`, to tell FastAPI
    that JSON is being sent, so it can be handled properly by Pydantic. I
    included the header, and from here I was able to add new URLs, which then
    immediately updated in the UI.

-   Initially I was returning a RedirectResponse for the `GET` request, but once
    I implemented the UI, I was getting a strange browser error, where the
    redirect was returned inside the fetch, but the browser didn't change. To
    fix this, I had to change the return of the call to just some JSON, which
    included the longUrl associated with the short code. The redirect is then
    handled with React. This means that the call returns a `200 OK` response
    instead of a more explicit `302 Found` redirect, but this seemed to be the
    most appropriate work around to get the redirect to work with the UI. When
    simply testing the `GET` call with the browser using
    `https://localhost:8000/{code}`, it loads the appropriate URL. I have
    commented out the initial RedirectResponse return for the endpoint, which
    can be changed and tested if deemed necessary.

#### 🔝 Limitations

-   For the scope of this project, a flat JSON file works fine; it's easy to
    implement and read/write from. In this context, a JSON file would become
    inefficient at a few thousand entries, at which point, upgrading to a SQLite
    DB would be more appropriate. I have abstracted the file access to separate
    file, so implementing a DB wouldn't affect any of the current logic.

-   I used the `AnyHttpUrl` type provided by Pydantic to validate the format of
    the longUrl provided as the payload for the `/shorten` endpoint. I liked
    this approach since it offered consistent type-safety, has auto error codes
    and is easy to implement. It works well in this context, but if full control
    over what format of URL can be stored, using a custom RegEx would be a
    better practice. Even better, a hybrid of a defined type and a RegEx could
    be used.

#### ❗ A Note on Exceptions

-   Originally, when the `shorten_and_save` function found a conflict in the
    stored URLs, I was simply raising a HTTPException, with a status_code (409)
    and some content. The same goes for the error handling function is main.py,
    which catches an error if the parsed URL does not meet the format defined in
    Pydantic's `AnyHttpUrl` type; a 422 response can be returned to signal a
    `Unprocessable Content` error. This is sufficient for the requirements of
    the API, but in order to better handle the errors on the Front End, I
    changed these HTTPExceptions to a JSONResponse, which still returns a HTTP
    code which is seen in the console and terminal, but allows for more detailed
    content to be parsed. Since it returns a JSON object as the content, React
    can see the error detail I have typed out and render it on the Front End
