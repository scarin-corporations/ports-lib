"""Bounded GitHub discovery. No game assets are downloaded or distributed."""
import argparse
import json
import math
import os
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def score(stars, pushed_at, now=None):
    now = now or datetime.now(timezone.utc)
    age = max(0, (now - datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))).days)
    return round(math.log10(stars + 1) * 20 + 30 * math.exp(-age / 180), 2)


def github(path):
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'ports-lib',
               'X-GitHub-Api-Version': '2022-11-28'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = 'Bearer ' + token
    request = urllib.request.Request('https://api.github.com' + path, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def normalize(repo, curated=None):
    curated = curated or {}
    return dict(name=repo['full_name'], url=repo['html_url'],
                description=repo.get('description') or '', stars=repo['stargazers_count'],
                pushedAt=repo['pushed_at'], archived=repo['archived'],
                license=(repo.get('license') or {}).get('spdx_id'),
                score=score(repo['stargazers_count'], repo['pushed_at']),
                kind=curated.get('kind', 'candidate'), consoles=curated.get('consoles', []),
                platforms=curated.get('platforms', []), evidence=curated.get('evidence'),
                reviewed=bool(curated))


def sync(root=ROOT):
    config = json.loads((root / 'data/curation.json').read_text())
    target = root / 'data/catalog.json'
    previous = json.loads(target.read_text())
    # Preserve previous observations on API errors; never publish an empty replacement.
    projects = {p['name'].lower(): p for p in previous['projects']}
    curated = {p['name'].lower(): p for p in config['projects']}
    excluded = {n.lower() for n in config['excluded']}
    errors = []
    successes = 0
    search_results = []
    capped_queries = []
    for entry in config['projects']:
        try:
            repo = github('/repos/' + entry['name'])
            projects[repo['full_name'].lower()] = normalize(repo, entry)
            successes += 1
        except (urllib.error.URLError, ValueError, KeyError) as exc:
            errors.append(f"{entry['name']}: {type(exc).__name__}")
    for item in config['queries']:
        query = item if isinstance(item, str) else item['q']
        sort = 'stars' if isinstance(item, str) else item.get('sort', 'stars')
        try:
            result = github('/search/repositories?' + urllib.parse.urlencode(
                {'q': query + ' fork:false', 'sort': sort, 'per_page': 100}))
            if result.get('incomplete_results'):
                errors.append(f'{query}: incomplete_results')
            items = list(result['items'])
            total = result['total_count']
            page = 1
            while len(items) < total and page < 10 and len(result['items']) == 100:
                page += 1
                try:
                    result = github('/search/repositories?' + urllib.parse.urlencode(
                        {'q': query + ' fork:false', 'sort': sort, 'per_page': 100, 'page': page}))
                    successes += 1
                    if result.get('incomplete_results'):
                        errors.append(f'{query} page {page}: incomplete_results')
                    items.extend(result['items'])
                except (urllib.error.URLError, ValueError, KeyError) as exc:
                    errors.append(f'{query} page {page}: {type(exc).__name__}')
                    break
                time.sleep(7)
            returned = len(items)
            search_results.append(dict(query=query, sort=sort, found=total, returned=returned, pages=page))
            if total > returned:
                capped_queries.append(query)
            for repo in items:
                name = repo['full_name'].lower()
                if name not in excluded:
                    projects[name] = normalize(repo, curated.get(name))
            successes += 1
        except (urllib.error.URLError, ValueError, KeyError) as exc:
            errors.append(f'{query}: {type(exc).__name__}')
        time.sleep(7)  # GitHub Search has a separate rate limit.
    projects = {k: v for k, v in projects.items() if k not in excluded}
    for name, project in projects.items():
        review = curated.get(name, {})
        project.update(reviewed=bool(review), kind=review.get('kind', 'candidate'),
                       consoles=review.get('consoles', []), platforms=review.get('platforms', []),
                       evidence=review.get('evidence'))
        project['score'] = score(project['stars'], project['pushedAt'])
    output = dict(updatedAt=datetime.now(timezone.utc).isoformat() if successes else previous['updatedAt'],
                  projects=sorted(projects.values(), key=lambda p: p['score'], reverse=True),
                  discovery=dict(status='partial' if errors and successes else 'failed' if errors else 'ok',
                                 candidates=sum(not p['reviewed'] for p in projects.values()),
                                 searches=search_results, cappedQueries=capped_queries), errors=errors)
    with tempfile.NamedTemporaryFile(mode='w', dir=target.parent, delete=False) as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)
        temporary = handle.name
    os.replace(temporary, target)
    print(f"{len(projects)} repositories; status={output['discovery']['status']}; errors={len(errors)}")
    return 1 if errors else 0


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    raise SystemExit(sync())
