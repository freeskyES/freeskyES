import feedparser
import os

# Velog RSS 피드 URL
rss_url = "https://v2.velog.io/rss/@freesky"
feed = feedparser.parse(rss_url)

# 캐시 파일
cache_file = "posts_cache.txt"

# 캐시 읽기
if os.path.exists(cache_file):
    with open(cache_file, "r", encoding="utf-8") as file:
        cached_posts = file.read().splitlines()
else:
    cached_posts = []

# 최신 5개 포스트 추출
latest_posts = [{"title": entry.title, "url": entry.link} for entry in feed.entries[:5]]

# 캐시에 없는 새 포스트만 추출
new_posts = [post for post in latest_posts if post["url"] not in cached_posts]

# 캐시 업데이트
with open(cache_file, "a", encoding="utf-8") as file:
    for post in new_posts:
        file.write(post["url"] + "\n")

# 뱃지 스타일로 변환 함수
def make_badge(post):
    # 뱃지에 들어갈 텍스트를 URL 인코딩
    from urllib.parse import quote
    title_encoded = quote(post["title"])
    return (
        f'<a href="{post["url"]}">'
        f'<img src="https://img.shields.io/badge/{title_encoded}-20C997?style=flat-square&logo=velog&logoColor=white" alt="{post["title"]}" />'
        f'</a>'
    )

# README.md 업데이트
if latest_posts:
    badges_html = "\n  ".join([make_badge(post) for post in latest_posts])
    new_section = (
        '\n<h3 align="center">✍️ Latest Blog Posts</h3>\n\n'
        '<p align="center">\n  '
        f'{badges_html}\n'
        '</p>\n'
    )

    # README.md 읽기
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()

    # 마커 찾기
    start_marker = "<!-- blog start -->"
    end_marker = "<!-- blog end -->"
    start_idx = readme_content.find(start_marker) + len(start_marker)
    end_idx = readme_content.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        updated_content = (
            readme_content[:start_idx]
            + new_section
            + readme_content[end_idx:]
        )
        with open("README.md", "w", encoding="utf-8") as file:
            file.write(updated_content)
        print("README.md updated with latest blog posts.")
    else:
        print("Error: Markers not found in README.md")
else:
    print("No new posts to add.")
