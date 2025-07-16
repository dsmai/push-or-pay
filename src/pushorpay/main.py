from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pushorpay.db import supabase_client
from pushorpay.scheduler import start_scheduler
from pushorpay.utils.utils import get_total_fines

# Create a FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="src/pushorpay/templates")
start_scheduler()  # Start background jobs immediately


# Create routes
@app.get("/", response_class=HTMLResponse)
def form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(
    name: str = Form(...),
    github: str | None = Form(None),
    leetcode_username: str | None = Form(None),
    daily_fine: float = Form(...),
):
    supabase_client.table("users").insert(  # type: ignore
        {
            "name": name,
            "github": github,
            "leetcode_username": leetcode_username,
            "daily_fine": daily_fine,
        }
    ).execute()
    return RedirectResponse("/leaderboard", status_code=302)


@app.get("/leaderboard", response_class=HTMLResponse)
def leaderboard(request: Request):
    fines = get_total_fines(supabase_client)

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            # Sort by fine amount, highest first
            "fines": sorted(fines, key=lambda x: -x[1]),
        },
    )
