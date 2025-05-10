from fastapi import Cookie, FastAPI, Response

app = FastAPI()

EXPIRATION_TIME = 60 * 60 * 24 * 7  # 1 week
HTTP_ONLY = True  # Set to True to prevent JavaScript access, should be True for security reasons
SECURE = True  # Set to True if using HTTPS
SAME_SITE = "none"  # or "Strict" or "None"
DOMAIN = "127.0.0.1"  # Replace with your domain
PATH = "/"  # Path for the cookie


@app.get("/set-cookie")
async def set_cookie(response: Response):
    """
    Set a cookie in the response.

    The cookie will be sent to the client and stored in the browser.

    The cookie will expire after the specified expiration time.

    The cookie will be HTTP-only, meaning it cannot be accessed via JavaScript.

    The cookie will be secure, meaning it will only be sent over HTTPS.
    """

    response.set_cookie(
        key="my_cookie",
        value="cookie_value",
        max_age=EXPIRATION_TIME,
        httponly=HTTP_ONLY,
        secure=SECURE,
        samesite=SAME_SITE,
        domain=DOMAIN,
        path=PATH,
    )
    return {"message": "Cookie set!"}


@app.get("/get-cookie")
async def get_cookie(my_cookie: str = Cookie(None)):
    """
    Retrieve the cookie value using the `Cookie()` dependency.

    The cookie value is passed as a parameter to the endpoint function.

    If the cookie is not found, it will be `None`.

    **Note:** The cookie will only be found if the name of the cookie matches the parameter name.
    """

    if my_cookie is None:
        return {"message": "No cookie found!"}
    # If the cookie is found, return its value
    return {"cookie_value": my_cookie}


@app.get("/delete-cookie")
async def delete_cookie(response: Response):
    """
    Delete the cookie by calling the `delete_cookie` method on the response object.

    This will remove the cookie from the client's browser.

    **Note:** The cookie will only be deleted if the path and domain match the original cookie.
    """
    response.delete_cookie(key="my_cookie")
    return {"message": "Cookie deleted!"}


@app.get("/bad-delete-cookie")
async def bad_delete_cookie(response: Response):
    """
    Attempt to delete a cookie with a different path.

    This will not work if the cookie was set with a specific path.
    """
    # This will not delete the cookie because the path is different
    response.delete_cookie(key="my_cookie", path="/wrong_path")
    return {"message": "Attempted to delete cookie with wrong path!"}
