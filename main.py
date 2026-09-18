from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
#from fastapi.templating import Jinja2Templates
import oracledb
import getpass

import auth.auth_router as auth_router


app = FastAPI()
#app.mount("/static", StaticFiles(directory="static"), name="static")
#templates = Jinja2Templates(directory="templates")

@app.get("/")
def pageAccueil():
    return { "Supinfo": "Bibliotheque" }

app.include_router(auth_router.router)

