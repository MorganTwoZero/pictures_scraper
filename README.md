# Pictures-scraper
An app that collects images and links from various sources(twitter, pixiv, mihoyo bbs, lofter, etc) merging them into a single stream. 

Built in fastapi and jinja templates(in v1) / vue(in v2)
## Why?
- it's tedious to check all sources one-by-one just to see mainly the same pictures
- twitter limit it's feed output so you can scroll up to 12-14 hours back at most
- it's hard to keep track of pictures that you have already seen
## Features
1. Scrape pictures and display them in a single stream
2. Add links to sources and authors
3. Mark seen
4. Like/retweet/follow
5. Adjust search queries in-app (settings file?)
6. Pick various sources to display(e.g. twiiter only, pixiv + lofter, etc)
7. Omit duplicates
8. Send to discord
