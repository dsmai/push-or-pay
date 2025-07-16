from supabase import Client


def get_total_fines(supabase_client: Client) -> list[tuple[str, float]]:
    users = supabase_client.table("users").select("*").execute().data
    fines: list[tuple[str, float]] = []
    for user in users:
        fine_amount_list = (
            supabase_client.table("checkins")
            .select("fine_amount")
            .eq("user_id", user["id"])
            .execute()
            .data
        )

        user_running_fine = sum(item["fine_amount"] for item in fine_amount_list)
        fines.append((user["name"], user_running_fine))
    return fines
