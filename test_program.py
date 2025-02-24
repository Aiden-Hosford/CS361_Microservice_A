import json
import time

PIPELINE_FILE = "pipeline.json"

def write_pipeline(data):
    with open(PIPELINE_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def read_pipeline():
    with open(PIPELINE_FILE, 'r') as f:
        return json.load(f)

# 1. Create a new character
print("Sending create_character command...")
request_data = {
    "command": "create_character",
    "char_name": "HeroA",
    "role": "Vanguard",
    "review": "Brave and daring.",
    "ranking": "A"
}
write_pipeline(request_data)

# Wait a moment for microservice to process
time.sleep(5)

# Read back the response
response_data = read_pipeline()
print("Response:", response_data.get("response"))

# 2. View the newly created character
print("\nSending view_character command...")
request_data = {
    "command": "view_character",
    "char_name": "HeroA"
}
write_pipeline(request_data)

time.sleep(5)

response_data = read_pipeline()
print("Response:", response_data.get("response"))

# 3. Update the existing character
print("\nSending update_character command...")
request_data = {
    "command": "update_character",
    "char_name": "HeroA",
    "review": "Updated review: even more epic!",
    "ranking": "S"
}
write_pipeline(request_data)

time.sleep(5)

response_data = read_pipeline()
print("Response:", response_data.get("response"))

# 4. Delete Character
print("\nSending delete_character command for HeroA...")
request_data = {
    "command": "delete_character",
    "char_name": "HeroA"
}
write_pipeline(request_data)

# Wait for microservice to process
time.sleep(5)

# Read the response
response_data = read_pipeline()
print("Delete Character Response:", response_data.get("response"))