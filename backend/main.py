from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .routers import items, users
from .routers import user_items
    

app = FastAPI()
router = APIRouter()

app.mount("/static",StaticFiles(directory="frontend", html=True), name="static")



app.include_router(items.router)
app.include_router(users.router)
app.include_router(user_items.router)


@app.get("/")
def read_index():
    return FileResponse("frontend/landing.html")


@app.get('/create-item')
def read_create_form():
    return FileResponse("frontend/index.html")









# when a user adds an item to their list 
# first we check if the item name exists in the db already 
# if so we add it to their list 
# if not we create a new item and then add it to their list 

