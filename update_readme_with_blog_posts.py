import feedparser
import os

# Fetch Velog RSS feed
rss_url = "https://v2.velog.io/rss/@freesky"
feed = feedparser.parse(rss_url)

# Cache file to store previously added post URLs
cache_file = "posts_cache.txt"

# Read the cache file, or create it if it doesn't exist
if os.path.exists(cache_file):
    with open(cache_file, "r") as file:
        cached_posts = file.read().splitlines()
else:
    cached_posts = []

# Extract the latest posts
latest_posts = [{"title": entry.title, "url": entry.link} for entry in feed.entries[:5]]

# Filter out posts that are already in the cache
new_posts = [post for post in latest_posts if post["url"] not in cached_posts]

# Debugging: Print cached and new posts to verify the logic
print("Cached Posts:", cached_posts)
print("New Posts to Add:", new_posts)

# Update the cache with the new posts
with open(cache_file, "a") as file:
    for post in new_posts:
        file.write(post["url"] + "\n")

# If there are new posts, update the README
if new_posts:
    markdown_content = "\n".join([f"- [{post['title']}]({post['url']})" for post in new_posts])

    # Add the section header
    section_header = "## ✍️ Latest Blog Posts\n"

    # Update README.md
    with open("README.md", "r") as file:
        readme_content = file.read()

    # Replace the content between the placeholders
    start_marker = "<!-- blog start -->"
    end_marker = "<!-- blog end -->"
    start_idx = readme_content.find(start_marker) + len(start_marker)
    end_idx = readme_content.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        updated_content = (
            readme_content[:start_idx]
            + f"\n{section_header}\n{markdown_content}\n"
            + readme_content[end_idx:]
        )

        with open("README.md", "w") as file:
            file.write(updated_content)
    else:
        print("Error: Markers not found in README.md")
else:
    print("No new posts to add.")
