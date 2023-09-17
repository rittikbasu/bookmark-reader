import json
from decouple import config
import supabase

username = config("USERNAME")
# Specify the path to your JSON file
json_file_path = (
    f"/Users/{username}/Library/Application Support/Arc/StorableSidebar.json"
)

# Specify the target parentID
target_parent_id = "7627CB15-392C-469D-B4FD-770480850673"

# Initialize an empty list to store matching elements
bookmarks = []

# Initialize the Supabase client with your Supabase URL and API key
supabase_url = config("SUPABASE_URL")
supabase_key = config("SUPABASE_API_KEY")
client = supabase.Client(supabase_url, supabase_key)

table_name = "bookmarks"

# Open and read the JSON file
with open(json_file_path, "r") as file:
    data = json.load(file)
    items = data.get("sidebarSyncState", {}).get(
        "items", []
    )  # Get the 'items' array under 'sidebarSyncState'

    # Iterate through the items and look for objects with the target parentID
    for item in items:
        if isinstance(item, dict) and "value" in item:
            value = item["value"]
            if "parentID" in value and value["parentID"] == target_parent_id:
                title = value["data"]["tab"]["savedTitle"]
                url = value["data"]["tab"]["savedURL"]
                created_at = value["createdAt"]

                # Remove everything starting from "- http" in savedTitle
                cleaned_title = title.split(" - http")[0]

                bookmarks.append(
                    {"url": url, "title": cleaned_title, "created_at": created_at}
                )

# Insert data into the table using upsert
response = client.table(table_name).upsert(bookmarks).execute()
