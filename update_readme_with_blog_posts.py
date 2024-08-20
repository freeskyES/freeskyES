import requests
import feedparser

# Fetch Velog RSS feed
rss_url = "https://v2.velog.io/rss/@freesky"
feed = feedparser.parse(rss_url)

# Extract the latest posts (adjust the range to display more posts if desired)
latest_posts = [{"title": entry.title, "url": entry.link} for entry in feed.entries[:5]]

# Generate Markdown content
markdown_content = "\n".join([f"- [{post['title']}]({post['url']})" for post in latest_posts])

# Update README.md
with open("README.md", "r") as file:
    readme_content = file.read()

# Replace the content between the placeholders
new_content = readme_content.replace("<!-- blog start -->", f"<!-- blog start -->\n{markdown_content}")

with open("README.md", "w", encoding='utf-8') as file:
    file.write(new_content)
