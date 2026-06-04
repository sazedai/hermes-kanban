#!/usr/bin/env python3
"""Fetch and parse arXiv API results for AI agent papers."""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import time
import hashlib
import os

QUERIES = [
    ("AI agent sub-agent delegation", 5),
    ("autonomous AI agent workflow", 5),
    ("multi-agent system context isolation", 5),
]

OUTPUT_DIR = os.path.expanduser("~/wiki/raw/papers")
os.makedirs(OUTPUT_DIR, exist_ok=True)

NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom',
}

all_papers = {}

for query, max_results in QUERIES:
    params = urllib.parse.urlencode({
        'search_query': f'all:{query}',
        'sortBy': 'submittedDate',
        'sortOrder': 'descending',
        'max_results': max_results,
    })
    url = f"https://export.arxiv.org/api/query?{params}"
    print(f"Fetching: {query}")
    print(f"URL: {url}")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read().decode('utf-8')
        root = ET.fromstring(data)

        for entry in root.findall('atom:entry', NS):
            arxiv_id = entry.find('atom:id', NS).text.split('/abs/')[-1]
            title = entry.find('atom:title', NS).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', NS).text.strip()
            summary = entry.find('atom:summary', NS).text.strip().replace('\n', ' ')
            authors = []
            for author in entry.findall('atom:author', NS):
                name = author.find('atom:name', NS).text.strip()
                authors.append(name)

            if arxiv_id not in all_papers:
                all_papers[arxiv_id] = {
                    'arxiv_id': arxiv_id,
                    'title': title,
                    'authors': authors,
                    'published': published,
                    'abstract': summary,
                    'source_url': f'https://arxiv.org/abs/{arxiv_id}',
                }
                print(f"  Found: {arxiv_id} - {title[:60]}...")
            else:
                print(f"  Duplicate: {arxiv_id}")

    except Exception as e:
        print(f"  ERROR: {e}")

    time.sleep(3)  # Be nice to arXiv API

print(f"\nTotal unique papers: {len(all_papers)}")

# Save all papers as JSON for further processing
papers_list = list(all_papers.values())
with open(os.path.expanduser("~/wiki/_papers_cache.json"), 'w') as f:
    json.dump(papers_list, f, indent=2)

print("Saved to ~/wiki/_papers_cache.json")
for p in papers_list:
    print(f"  {p['arxiv_id']}: {p['title'][:80]}")
