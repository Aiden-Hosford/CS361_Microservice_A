import json
import os
import time

PIPELINE_FILE = "pipeline.json"
DATA_STORE_FILE = "data_store.json"

def load_characters():
    """Load characters from data_store.json (if it exists)."""
    if os.path.exists(DATA_STORE_FILE):
        with open(DATA_STORE_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                # If file is empty or corrupted, return an empty list
                return []
    return []

def save_characters(characters):
    """Save character data to data_store.json."""
    with open(DATA_STORE_FILE, 'w') as f:
        json.dump(characters, f, indent=2)

def read_pipeline():
    """Read the pipeline.json for instructions."""
    if not os.path.exists(PIPELINE_FILE):
        return {}
    with open(PIPELINE_FILE, 'r') as f:
        try:
            data = json.load(f)
            return data
        except json.JSONDecodeError:
            return {}

def write_pipeline(data):
    """Write back to pipeline.json."""
    with open(PIPELINE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_character(request):
    """
    Expected request format:
    {
      "command": "create_character",
      "char_name": "...",
      "role": "...",
      "review": "...",
      "ranking": "..."
    }
    """
    characters = load_characters()

    char_name = request.get("char_name")
    role = request.get("role")
    review = request.get("review")
    ranking = request.get("ranking")

    # Basic validation
    if not char_name or not role or not review or not ranking:
        return {"status": "error", "message": "Missing required fields."}

    # Check if character already exists
    for char in characters:
        if char["name"].lower() == char_name.lower():
            return {"status": "error", "message": "Character already exists."}

    # Create new character
    new_char = {
        "name": char_name,
        "role": role,
        "review": review,
        "ranking": ranking
    }
    characters.append(new_char)
    save_characters(characters)
    return {"status": "success", "message": f"Character '{char_name}' created."}

def view_character(request):
    """
    Expected request format:
    {
      "command": "view_character",
      "char_name": "..."
    }
    """
    characters = load_characters()
    char_name = request.get("char_name")
    if not char_name:
        return {"status": "error", "message": "No character name provided."}

    for char in characters:
        if char["name"].lower() == char_name.lower():
            return {
                "status": "success",
                "data": {
                    "name": char["name"],
                    "role": char["role"],
                    "review": char["review"],
                    "ranking": char["ranking"]
                }
            }
    return {"status": "error", "message": f"Character '{char_name}' not found."}

def update_character(request):
    """
    Expected request format:
    {
      "command": "update_character",
      "char_name": "...",
      "role": "...",
      "review": "...",
      "ranking": "..."
    }
    At least one of role, review, or ranking might be specified to update.
    """
    characters = load_characters()

    char_name = request.get("char_name")
    if not char_name:
        return {"status": "error", "message": "No character name provided."}

    updated = False
    for char in characters:
        if char["name"].lower() == char_name.lower():
            # Update fields if present
            if "role" in request and request["role"]:
                char["role"] = request["role"]
            if "review" in request and request["review"]:
                char["review"] = request["review"]
            if "ranking" in request and request["ranking"]:
                char["ranking"] = request["ranking"]
            updated = True
            break

    if updated:
        save_characters(characters)
        return {"status": "success", "message": f"Character '{char_name}' updated."}
    else:
        return {"status": "error", "message": f"Character '{char_name}' not found."}

def delete_character(request):
    """
    Expected request format:
    {
      "command": "delete_character",
      "char_name": "..."
    }
    """
    characters = load_characters()
    char_name = request.get("char_name")

    if not char_name:
        return {"status": "error", "message": "No character name provided."}

    # Find and remove character
    updated_characters = [c for c in characters if c["name"].lower() != char_name.lower()]

    if len(updated_characters) < len(characters):
        save_characters(updated_characters)
        return {"status": "success", "message": f"Character '{char_name}' deleted."}
    else:
        return {"status": "error", "message": f"Character '{char_name}' not found."}

def main():
    print("Microservice A is running. Monitoring pipeline.json for commands...")
    while True:
        pipeline_data = read_pipeline()
        command = pipeline_data.get("command", "")

        if command == "create_character":
            response = create_character(pipeline_data)
            pipeline_data["response"] = response
            pipeline_data["command"] = ""  # Reset command
            write_pipeline(pipeline_data)

        elif command == "view_character":
            response = view_character(pipeline_data)
            pipeline_data["response"] = response
            pipeline_data["command"] = ""
            write_pipeline(pipeline_data)

        elif command == "update_character":
            response = update_character(pipeline_data)
            pipeline_data["response"] = response
            pipeline_data["command"] = ""
            write_pipeline(pipeline_data)

        elif command == "delete_character":
            response = delete_character(pipeline_data)
            pipeline_data["response"] = response
            pipeline_data["command"] = ""
            write_pipeline(pipeline_data)

        time.sleep(1)

if __name__ == "__main__":
    main()

