import os
import asyncio
from datetime import datetime, timezone
import httpx
from dotenv import load_dotenv

load_dotenv()

"""Handle API checkers (Github commit/Leetcode submission)"""


async def leetcode_solved_today(
    username: str = "dsmai", max_retries: int = 3
) -> bool | None:
    """
    Check if user solved LeetCode problems today with retry logic

    Returns:
    - True: User solved problems today
    - False: User did NOT solve problems today
    - None: API unavailable (don't penalize user)
    """
    if not username:
        return False

    LEETCODE_API_URL = os.environ["LEETCODE_API_URL"]
    leetcode_url = f"{LEETCODE_API_URL}/{username}"

    for attempt in range(max_retries):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 1. Creates HTTP client with 10-second timeout
                # 2. Assigns it to variable 'client'
                # 3. Automatically closes client when done (even if error occurs)

                response = await client.get(leetcode_url)

                if response.status_code == 200:
                    data = response.json()
                    leetcode_submission_calendar = data.get("submissionCalendar", {})

                    # Get today timestamp in PST
                    today_ts = int(
                        datetime.now(timezone.utc)
                        .replace(hour=0, minute=0, second=0, microsecond=0)
                        .timestamp()
                    )

                    # Dictionary look up to see if today_ts is in leetcode_submission_calendar
                    # Had to convert back to string
                    problems_solved_today = leetcode_submission_calendar[str(today_ts)]

                    print(f"{username} solved {problems_solved_today} problems today")
                    return str(today_ts) in leetcode_submission_calendar

                elif response.status_code == 404:
                    print(f"Leetcode user '{username}' not found!")
                    return False

                else:
                    print(
                        f"⚠️ LeetCode API error {response.status_code}, attempt {attempt + 1}/{max_retries}"
                    )
        except (httpx.TimeoutException, httpx.ConnectError) as e:
            print(
                f"🔌 LeetCode API connection failed, attempt {attempt + 1}/{max_retries}: {e}"
            )

        # Wait for retry (exponential back off)
        if attempt < max_retries - 1:
            wait_time = 2**attempt
            await asyncio.sleep(wait_time)

    # All retries failed
    print(f"🚫 LeetCode API unavailable for {username} after {max_retries} attempts")
    return None


if __name__ == "__main__":
    print("This only runs when executed directly!")
    result = asyncio.run(leetcode_solved_today())
    print(f"Result: {result}")
