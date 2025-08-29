import json
import os
import re

# Load json file
with open("conversations.json", "r", encoding="utf-8") as f:
    data = reversed(json.loads(f.read()))

# Create directory for markdown files
os.makedirs("conversations", exist_ok=True)

# Iterate over each conversation
counter = 0
for conversation in data:
    title = conversation["title"]
    messages = conversation["mapping"]

    if title == "":
        title = "Ohne Titel"

    md_content = f"# {title}\n"

    # Format title for filename
    filename_title = title.replace("ä", "ae").replace("Ä", "Ae").replace("ö", "oe").replace("Ö", "Oe").replace("ü", "ue").replace("Ü", "Ue").replace("ß", "ss")
    filename_title = re.sub(r'[^.A-Za-z0-9_-]', '_', filename_title)

    # Add number to filename title
    filename_title = (f"{counter:05}") + "_" + filename_title
    counter += 1


    for msg in messages:
        # Get actual message
        message = messages[msg]

        # Check whether the message is really a message
        if (not ("message" in message)):
            continue
        if message["message"] == None:
            continue
        if message["message"]["create_time"] == None:
            continue
        if (not ("parts" in message["message"]["content"])):
            continue
        if message["message"]["content"]["parts"] == None:
            continue

        # Get the message itself
        if message["message"]["author"]["role"] == "user":
            md_content += "# User:\n"
        else:
            md_content += "# ChatGPT:\n"

        # Replace images
        parts2 = []
        for part in message["message"]["content"]["parts"]:
            if isinstance(part, dict):
                if (not ("asset_pointer" in part)):
                    continue

                string = part["asset_pointer"].replace("file-service://", "")
                parts2.append(string)
            else:
                parts2.append(part)


        md_content += "\n".join(parts2)
        md_content += "\n\n"

    filename = f"conversations/{filename_title}.md"
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write(md_content)
