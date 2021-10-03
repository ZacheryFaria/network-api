from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def root(request: Request):
    return {"message": "hello world", "root_path": request.scope.get("root_path")}

