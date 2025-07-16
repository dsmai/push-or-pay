from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore
from pushorpay.db import supabase_client
from pushorpay.checker import get_leetcode_count_today
from pushorpay.notifier import post_to_discord
from datetime import date
import asyncio
from pushorpay.utils.utils import get_total_fines
from typing import TypedDict


class User(TypedDict):
    id: int
    name: str
    github: str | None
    leetcode_username: str | None
    daily_fine: float


class CheckinInsert(TypedDict):
    user_id: int
    date: str
    did_leetcode: bool
    fine_amount: float


def start_scheduler() -> None:
    scheduler = BackgroundScheduler(timezone="America/Los_Angeles")
    scheduler.add_job(run_daily, "cron", hour=0, minute=0)  # type: ignore


def run_daily() -> None:
    asyncio.run(daily_task())


async def daily_task() -> None:
    users = supabase_client.table("users").select("*").execute().data
    missed: list[str] = []
    for user in users:
        leetcode_count_today = await get_leetcode_count_today(user["leetcode_username"])
        did_leetcode_today = True if leetcode_count_today else False
        fine = user["daily_fine"] if not did_leetcode_today else 0.0
        new_checkin: CheckinInsert = {
            "user_id": user["id"],
            "date": str(date.today()),
            "did_leetcode": did_leetcode_today,
            "fine_amount": fine,
        }

        supabase_client.table("checkins").insert(new_checkin).execute()  # type: ignore

        if fine:
            missed.append(f"{user["name"]} (+${fine:.2f})")

    # Calculation for leaderboard:
    fines = get_total_fines(supabase_client)

    # Format and send Discord message
    missed_message = (
        "\n".join(f"❌ {entry}" for entry in missed) or "✅ Everyone good today!"
    )
    leaderboard_message = "\n".join(
        f"- {name}: ${running_fine:.2f}"
        for name, running_fine in sorted(fines, key=lambda x: -x[1])
    )
    message = f"📊 Daily Check-in Results\n{missed_message}\n\n🏆 Leaderboard:\n{leaderboard_message}"
    await post_to_discord(message)
