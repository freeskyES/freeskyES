import feedparser
import os

# Fetch Velog RSS feed
rss_url = "https://v2.velog.io/rss/@freesky"
feed = feedparser.parse(rss_url)

# Read the cache file
if os.path.exists("posts_cache.txt"):
    with open("posts_cache.txt", "r") as file:
        cached_posts = file.read().splitlines()
else:
    cached_posts = []

# Extract the latest posts
latest_posts = [{"title": entry.title, "url": entry.link} for entry in feed.entries[:5]]

# Filter out posts that are already in the cache
new_posts = [post for post in latest_posts if post["url"] not in cached_posts]

# Update the cache with the new posts
with open("posts_cache.txt", "a") as file:
    for post in new_posts:
        file.write(post["url"] + "\n")

# If there are new posts, update the README
if new_posts:
    markdown_content = "\n".join([f"- [{post['title']}]({post['url']})" for post in new_posts])

    # Update README.md
    with open("README.md", "r") as file:
        readme_content = file.read()

    # Replace the content between the placeholders
    new_content = readme_content.replace("<!-- blog start -->", f"<!-- blog start -->\n{markdown_content}")

    with open("README.md", "w") as file:
        file.write(new_content)
else:
    print("No new posts to add.")
