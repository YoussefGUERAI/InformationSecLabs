#!/usr/bin/env python3
"""Challenge B - minimal same-host web spider (BFS)."""
import sys
import time
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse

import requests
from bs4 import BeautifulSoup

MAX_PAGES = 10      # visit at most 10 HTML pages
DELAY = 2           # seconds between requests (minimum)
TIMEOUT = 5         # seconds per request
HEADERS = {"User-Agent": "ChallengeB-Spider/1.0 (educational)"}


def normalise(base, href):
    """Resolve href against base, drop #fragment, return absolute URL or None."""
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    absolute = urljoin(base, href)          # relative -> absolute
    absolute, _frag = urldefrag(absolute)   # drop #fragment
    p = urlparse(absolute)
    if p.scheme not in ("http", "https"):
        return None
    # lower-case scheme/host, default path "/" so /a and /a# collapse cleanly
    return p._replace(scheme=p.scheme.lower(),
                      netloc=p.netloc.lower(),
                      path=p.path or "/").geturl()


def crawl(start_url):
    start_url = normalise(start_url, start_url)
    host = urlparse(start_url).netloc

    queue = deque([start_url])   # frontier (FIFO -> breadth-first)
    seen = {start_url}           # every URL ever queued (dedup)
    visited = []                 # HTML pages actually fetched
    site_map = {}                # page -> list of same-host links found
    session = requests.Session()
    session.headers.update(HEADERS)
    last_request = 0.0

    while queue and len(visited) < MAX_PAGES:
        url = queue.popleft()

        # politeness: enforce >= DELAY seconds since previous request
        wait = DELAY - (time.monotonic() - last_request)
        if wait > 0:
            time.sleep(wait)

        try:
            last_request = time.monotonic()
            resp = session.get(url, timeout=TIMEOUT)
        except requests.RequestException as e:
            print(f"[ERR ] {url} -> {e.__class__.__name__}")
            continue

        # only HTML pages count and get parsed
        ctype = resp.headers.get("Content-Type", "")
        if resp.status_code != 200 or "text/html" not in ctype:
            print(f"[SKIP] {url} ({resp.status_code}, {ctype or 'no type'})")
            continue

        # redirects may move us off-host: re-check the final URL
        final = normalise(resp.url, resp.url)
        if urlparse(final).netloc != host:
            print(f"[SKIP] {url} redirected off-host -> {final}")
            continue

        visited.append(url)
        print(f"[{len(visited):2}/{MAX_PAGES}] {url}")

        soup = BeautifulSoup(resp.text, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            link = normalise(final, a["href"])
            if link is None or urlparse(link).netloc != host:
                continue                     # same host only
            links.append(link)
            if link not in seen:             # avoid duplicates
                seen.add(link)
                queue.append(link)
        site_map[url] = sorted(set(links))

    return visited, site_map


def main():
    if len(sys.argv) != 2:
        sys.exit(f"usage: {sys.argv[0]} <homepage-url>")
    visited, site_map = crawl(sys.argv[1])

    print(f"\n=== Site map ({len(visited)} pages) ===")
    for page, links in site_map.items():
        print(page)
        for l in links:
            print(f"   -> {l}")


if __name__ == "__main__":
    main()
