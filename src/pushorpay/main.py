from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pushorpay.checker import get_leetcode_count_today
from pushorpay.db import supabase_client
from pushorpay.scheduler import start_scheduler
from pushorpay.utils.utils import get_total_fines
from typing import TypedDict


class LeaderboardEntry(TypedDict):
    name: str
    fine: float
    leetcode_problems_count_today: int


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
async def leaderboard(request: Request):
    users = supabase_client.table("users").select("*").execute().data
    fines = get_total_fines(supabase_client)

    # Fetch leetcode problem counts today so far for each user
    leetcode_problems_count_today = {}
    for user in users:
        leetcode_username = user[
            "leetcode_username"
        ]  # Need to verify this, leetcode_username should be required
        if leetcode_username:
            count = await get_leetcode_count_today(leetcode_username)
        else:
            count = 0
        leetcode_problems_count_today[user["name"]] = count

    leaderboard_data: list[LeaderboardEntry] = [
        {
            "name": name,
            "fine": fine,
            "leetcode_problems_count_today": leetcode_problems_count_today[name],
        }
        for name, fine in fines
    ]

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            # Sort by fine amount, highest first
            "leaderboard": sorted(leaderboard_data, key=lambda x: -x["fine"]),
        },
    )
