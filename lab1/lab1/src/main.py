import uvicorn
from fastapi import FastAPI, HTTPException
app = FastAPI()

#all HTTP code justifications were taken from this website: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses

#HTTP response 422 means "Bad Request" which means that the server cannot or will not process it due to a client side issue
#ie: not filling in the name parameter
@app.get("/hello")
async def hello(name):
    if not name:
        raise HTTPException(status_code=422, detail="Bad Request: Invalid or missing name.")
    return {"name": "Hello " + name}

#501 is the "Not Implemented" error that all server are require to support
@app.get("/")
async def root():
    raise HTTPException(status_code=501, detail="not implemented")


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)